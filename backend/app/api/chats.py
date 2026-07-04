from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.database import get_db, get_tenant_slug, get_qdrant_client
from app.gateways.model_gateway import ModelGateway
from app.gateways.embedding_gateway import EmbeddingGateway
from app.gateways.mcp_gateway import MCPGateway
from tracenest import logger
import time
import json
import uuid

router = APIRouter(tags=["Chats"])

class MessageModel(BaseModel):
    role: str # "user", "assistant", "system"
    content: str

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    messages: List[MessageModel]
    use_rag: bool = True

@router.post("/chat")
@router.post("/chats")
async def chat_interaction(payload: ChatRequest):
    """Processes chat request with RAG retrieval, MCP verification, and multi-model fallback."""
    slug = get_tenant_slug()
    db = get_db()
    session_id = payload.session_id or str(uuid.uuid4())
    
    if not payload.messages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Messages list cannot be empty"
        )
        
    last_user_msg = ""
    for msg in reversed(payload.messages):
        if msg.role == "user":
            last_user_msg = msg.content
            break
            
    # --- Step 1: Check for MCP tool invocation inside the user message ---
    # Example format: "run_tool: read_file arguments: {"path": "app/config.py"}"
    if "run_tool:" in last_user_msg:
        try:
            parts = last_user_msg.split("run_tool:")
            tool_parts = parts[1].strip().split("arguments:")
            tool_name = tool_parts[0].strip()
            args_str = tool_parts[1].strip() if len(tool_parts) > 1 else "{}"
            arguments = json.loads(args_str)
            
            # Run through MCP Risk scoring
            mcp_result = await MCPGateway.process_tool_call(
                tenant_id=slug,
                tool_name=tool_name,
                arguments=arguments,
                requested_by="user"
            )
            
            # Save request/response in history
            chat_record = {
                "session_id": session_id,
                "tenant_id": slug,
                "messages": [m.model_dump() for m in payload.messages],
                "mcp_verification": mcp_result,
                "timestamp": time.time()
            }
            await db.chats.insert_one(chat_record)
            
            return {
                "session_id": session_id,
                "response": f"[MCP Tool Invocation] Risk: {mcp_result['risk_level']}. Status: {mcp_result['status']}.",
                "mcp_verification": mcp_result
            }
        except Exception as e:
            logger.error(f"Failed parsing tool call: {str(e)}")
            # fall through to standard chat if parsing fails
            
    # --- Step 2: RAG Context Retrieval ---
    rag_context = ""
    if payload.use_rag and last_user_msg:
        try:
            model_name = "all-MiniLM-L6-v2"
            vector = EmbeddingGateway.get_embedding(last_user_msg, model_name)
            collection_name = f"org_{slug.replace('-', '_')}_vectors"
            
            qdrant_client = get_qdrant_client()
            # Search Qdrant
            hits = qdrant_client.search(
                collection_name=collection_name,
                query_vector=vector,
                limit=3
            )
            
            if hits:
                context_chunks = []
                for hit in hits:
                    chunk_text = hit.payload.get("content", "")
                    filename = hit.payload.get("filename", "unknown")
                    context_chunks.append(f"[Source: {filename}]\n{chunk_text}")
                
                rag_context = "\n\n".join(context_chunks)
                logger.info(f"RAG context retrieved: {len(hits)} chunks for tenant {slug}")
        except Exception as e:
            # collection might not exist yet
            logger.warning(f"RAG search skipped or failed for tenant {slug}: {str(e)}")
            
    # --- Step 3: Call Multi-Model LLM Gateway ---
    messages_payload = [m.model_dump() for m in payload.messages]
    
    if rag_context:
        # Prepend system instructions or append context to the user query
        # Let's insert the context into the user's query or system prompt
        context_prompt = f"Use the following retrieved document context to answer the question:\n\n{rag_context}\n\nUser Question: {last_user_msg}"
        # Modify the last user message to include context
        for msg in reversed(messages_payload):
            if msg["role"] == "user":
                msg["content"] = context_prompt
                break

    # Call LLM fallback sequence
    llm_response = await ModelGateway.generate(messages_payload, tenant_id=slug)
    
    # Save conversation history to MongoDB
    chat_record = {
        "session_id": session_id,
        "tenant_id": slug,
        "messages": [m.model_dump() for m in payload.messages] + [{"role": "assistant", "content": llm_response["content"]}],
        "provider": llm_response["provider"],
        "model": llm_response["model"],
        "latency": llm_response["latency"],
        "timestamp": time.time()
    }
    await db.chats.insert_one(chat_record)
    
    return {
        "session_id": session_id,
        "response": llm_response["content"],
        "provider": llm_response["provider"],
        "model": llm_response["model"],
        "latency": llm_response["latency"]
    }

@router.get("/chat/sessions")
@router.get("/chats/sessions")
async def list_chat_sessions():
    """Lists unique chat session IDs for the current tenant."""
    slug = get_tenant_slug()
    db = get_db()
    sessions = await db.chats.distinct("session_id", {"tenant_id": slug})
    return {"sessions": sessions}

@router.get("/chat/{session_id}")
@router.get("/chats/{session_id}")
async def get_chat_history(session_id: str):
    """Retrieves chat history for a session."""
    slug = get_tenant_slug()
    db = get_db()
    
    history = await db.chats.find({"session_id": session_id, "tenant_id": slug}).sort("timestamp", 1).to_list(100)
    for doc in history:
        doc["_id"] = str(doc["_id"])
        
    return history
