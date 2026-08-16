from langsmith import traceable
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
@traceable
async def chat_interaction(payload: ChatRequest):
    logger.debug(f"Entering chat_interaction")
    """Processes chat request with RAG retrieval, MCP verification, and multi-model fallback."""
    slug = get_tenant_slug()
    logger.debug(f"Resolved tenant slug: {slug}")
    db = get_db()
    session_id = payload.session_id or str(uuid.uuid4())
    logger.info(f"Starting chat interaction. Tenant: {slug} | Session ID: {session_id} | Payload size: {len(payload.messages)} messages")
    
    if not payload.messages:
        logger.warning(f"Rejecting chat request for tenant {slug}. Reason: Empty messages list provided in payload.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Messages list cannot be empty"
        )
    logger.debug("Payload message list is valid.")
        
    last_user_msg = ""
    logger.debug("Extracting the last user message from the payload stack...")
    for msg in reversed(payload.messages):
        if msg.role == "user":
            last_user_msg = msg.content
            logger.info(f"Successfully extracted last user message: {last_user_msg[:50]}...")
            break
            
    # --- Step 1: Check for MCP tool invocation inside the user message ---
    logger.debug("Step 1: Checking if the user message contains a requested MCP tool invocation pattern.")
    # Example format: "run_tool: read_file arguments: {"path": "app/config.py"}"
    if "run_tool:" in last_user_msg:
        logger.info("MCP Tool invocation detected in user message. Initiating parsing sequence.")
        try:
            parts = last_user_msg.split("run_tool:")
            tool_parts = parts[1].strip().split("arguments:")
            tool_name = tool_parts[0].strip()
            args_str = tool_parts[1].strip() if len(tool_parts) > 1 else "{}"
            arguments = json.loads(args_str)
            logger.debug(f"Parsed MCP Tool Name: {tool_name}")
            logger.debug(f"Parsed MCP Tool Arguments: {arguments}")
            
            # Run through MCP Risk scoring
            logger.info(f"Passing {tool_name} to MCPGateway for strict tenant risk evaluation.")
            mcp_result = await MCPGateway.process_tool_call(
                tenant_id=slug,
                tool_name=tool_name,
                arguments=arguments,
                requested_by="user"
            )
            logger.info(f"MCPGateway completed evaluation. Risk Level: {mcp_result['risk_level']}. Status: {mcp_result['status']}")
            
            # Save request/response in history
            logger.debug(f"Persisting MCP interaction to MongoDB chat history collection for session {session_id}.")
            chat_record = {
                "session_id": session_id,
                "tenant_id": slug,
                "messages": [m.model_dump() for m in payload.messages],
                "mcp_verification": mcp_result,
                "timestamp": time.time()
            }
            await db.chats.insert_one(chat_record)
            logger.debug("Successfully saved MCP chat record to database.")
            
            return {
                "session_id": session_id,
                "response": f"[MCP Tool Invocation] Risk: {mcp_result['risk_level']}. Status: {mcp_result['status']}.",
                "mcp_verification": mcp_result
            }
        except Exception as e:
            logger.error(f"Failed parsing tool call for tenant {slug}. Falling back to standard chat processing. Error: {str(e)}", exc_info=True)
            # fall through to standard chat if parsing fails
            
    # --- Step 2: RAG Context Retrieval ---
    logger.debug("Step 2: Starting RAG context retrieval sequence.")
    rag_context = ""
    if payload.use_rag and last_user_msg:
        logger.info(f"RAG is enabled. Attempting semantic search across Qdrant vectors for tenant {slug}.")
        try:
            model_name = "all-MiniLM-L6-v2"
            logger.debug(f"Generating embeddings for query using model: {model_name}")
            vector = EmbeddingGateway.get_embedding(last_user_msg, model_name)
            collection_name = f"org_{slug.replace('-', '_')}_vectors"
            
            logger.debug(f"Connecting to Qdrant collection: {collection_name}")
            qdrant_client = get_qdrant_client()
            # Search Qdrant
            logger.debug("Executing Qdrant similarity search algorithm (limit=3)...")
            hits = qdrant_client.search(
                collection_name=collection_name,
                query_vector=vector,
                limit=3
            )
            logger.debug(f"Qdrant returned {len(hits)} raw hits.")
            
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
    logger.info("Step 3: Constructing final payload and dispatching to Multi-Model LLM Gateway.")
    messages_payload = [m.model_dump() for m in payload.messages]
    
    if rag_context:
        logger.debug("Injecting structured RAG context directly into the user's prompt stack.")
        # Prepend system instructions or append context to the user query
        # Let's insert the context into the user's query or system prompt
        context_prompt = f"Use the following retrieved document context to answer the question:\n\n{rag_context}\n\nUser Question: {last_user_msg}"
        # Modify the last user message to include context
        for msg in reversed(messages_payload):
            if msg["role"] == "user":
                msg["content"] = context_prompt
                break

    # Call LLM fallback sequence
    logger.info("Executing ModelGateway.generate() cascade. Standby for LLM inference...")
    llm_response = await ModelGateway.generate(messages_payload, tenant_id=slug)
    logger.info(f"ModelGateway successfully returned response from provider: {llm_response['provider']} (Model: {llm_response['model']}) in {llm_response['latency']}s")
    
    # Save conversation history to MongoDB
    logger.debug(f"Committing LLM response and full chat context to MongoDB for session {session_id}.")
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
    logger.debug(f"Entering list_chat_sessions")
    """Lists unique chat session IDs for the current tenant."""
    slug = get_tenant_slug()
    db = get_db()
    sessions = await db.chats.distinct("session_id", {"tenant_id": slug})
    return {"sessions": sessions}

@router.get("/chat/{session_id}")
@router.get("/chats/{session_id}")
async def get_chat_history(session_id: str):
    logger.debug(f"Entering get_chat_history")
    """Retrieves chat history for a session."""
    slug = get_tenant_slug()
    db = get_db()
    
    history = await db.chats.find({"session_id": session_id, "tenant_id": slug}).sort("timestamp", 1).to_list(100)
    for doc in history:
        doc["_id"] = str(doc["_id"])
        
    return history
