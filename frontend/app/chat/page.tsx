'use client';

import React, { useState } from 'react';
import Layout from '../../components/Layout';
import { useStore, ChatMessage } from '../../components/store';
import { Send, FileText, Check, X, ShieldAlert, Cpu, AlertCircle, Quote } from 'lucide-react';
import { ReactFlow, Background, Controls } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

export default function ChatPage() {
  const { chatHistory, sendChatMessage, approvals, approveRequest, rejectRequest, isLoading } = useStore();
  const [input, setInput] = useState('');

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendChatMessage(input);
    setInput('');
  };

  const getApprovalStatus = (id?: string) => {
    if (!id) return null;
    return approvals.find(a => a.id === id);
  };

  return (
    <Layout>
      <div className="flex flex-col h-[calc(100vh-8rem)]">
        {/* Chat Feed */}
        <div className="flex-1 overflow-y-auto space-y-6 pb-6 pr-2">
          {chatHistory.map((msg) => {
            const isUser = msg.sender === 'user';
            const approval = getApprovalStatus(msg.approvalId);

            return (
              <div
                key={msg.id}
                className={`flex gap-4 max-w-4xl ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
              >
                {/* Profile Icon */}
                <div className={`h-9 w-9 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 shadow-md ${
                  isUser 
                    ? 'bg-gradient-to-tr from-indigo-500 to-purple-600 text-white' 
                    : 'bg-slate-900 border border-slate-800 text-indigo-400'
                }`}>
                  {isUser ? 'U' : 'AI'}
                </div>

                {/* Message Body */}
                <div className="space-y-3 flex-1 min-w-0">
                  <div className={`p-4 rounded-2xl border text-sm leading-relaxed shadow-sm ${
                    isUser
                      ? 'bg-indigo-600/15 border-indigo-500/20 text-indigo-100'
                      : 'bg-slate-900/40 border-slate-800 text-slate-200'
                  }`}>
                    {msg.content}
                  </div>

                  {/* Flow Data representation (React Flow tool execution) */}
                  {!isUser && msg.flowData && (
                    <div className="border border-slate-800 bg-slate-950/60 rounded-xl overflow-hidden shadow-inner">
                      <div className="px-4 py-2 border-b border-slate-800 bg-slate-900/30 flex items-center gap-2">
                        <Cpu className="h-4 w-4 text-indigo-400" />
                        <span className="text-xs font-semibold text-slate-300">MCP Tool Execution Representation</span>
                      </div>
                      <div className="h-56 w-full relative">
                        <ReactFlow
                          nodes={msg.flowData.nodes}
                          edges={msg.flowData.edges}
                          fitView
                          proOptions={{ hideAttribution: true }}
                          nodesDraggable={false}
                          nodesConnectable={false}
                        >
                          <Background color="#334155" gap={16} />
                          <Controls showInteractive={false} />
                        </ReactFlow>
                      </div>
                    </div>
                  )}

                  {/* Approval Cards */}
                  {!isUser && approval && (
                    <div className="border border-rose-500/20 bg-rose-500/5 p-4 rounded-2xl space-y-3">
                      <div className="flex items-start gap-2.5">
                        <ShieldAlert className="h-5 w-5 text-rose-400 shrink-0 mt-0.5" />
                        <div>
                          <h4 className="text-xs font-bold text-slate-200">Execution Block: Approval Staged</h4>
                          <p className="text-xs text-slate-400 mt-1">{approval.description}</p>
                        </div>
                      </div>

                      <div className="flex gap-2">
                        {approval.status === 'pending' ? (
                          <>
                            <button
                              onClick={() => approveRequest(approval.id)}
                              className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold py-1.5 px-3.5 rounded-lg flex items-center gap-1 transition"
                            >
                              <Check className="h-3.5 w-3.5" /> Approve & Execute
                            </button>
                            <button
                              onClick={() => rejectRequest(approval.id)}
                              className="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold py-1.5 px-3.5 rounded-lg flex items-center gap-1 transition"
                            >
                              <X className="h-3.5 w-3.5" /> Reject
                            </button>
                          </>
                        ) : (
                          <span className={`text-xs font-semibold px-2.5 py-1 rounded-lg border ${
                            approval.status === 'approved' 
                              ? 'bg-emerald-500/10 border-emerald-500/25 text-emerald-400' 
                              : 'bg-rose-500/10 border-rose-500/25 text-rose-400'
                          }`}>
                            Staged Status: {approval.status.toUpperCase()}
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  {/* RAG Citations */}
                  {!isUser && msg.citations && msg.citations.length > 0 && (
                    <div className="space-y-2">
                      <div className="text-[10px] uppercase font-bold tracking-wider text-slate-500 flex items-center gap-1">
                        <Quote className="h-3 w-3" /> Cognitive Grounding Sources
                      </div>
                      <div className="grid sm:grid-cols-2 gap-2">
                        {msg.citations.map((c) => (
                          <div key={c.id} className="p-3 border border-slate-800/80 bg-slate-900/20 rounded-xl">
                            <div className="flex items-center justify-between">
                              <span className="text-xs font-semibold text-indigo-400 flex items-center gap-1">
                                <FileText className="h-3.5 w-3.5" /> {c.docName}
                              </span>
                              <span className="text-[9px] font-mono bg-slate-800 px-1 rounded text-slate-400">
                                Match: {Math.floor(c.score * 100)}%
                              </span>
                            </div>
                            <p className="text-[11px] text-slate-400 mt-1.5 italic line-clamp-2">
                              "{c.snippet}"
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Timestamp */}
                  <p className={`text-[10px] text-slate-500 ${isUser ? 'text-right' : 'text-left'}`}>
                    {msg.timestamp}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Input Bar */}
        <form onSubmit={handleSend} className="border-t border-slate-800/80 pt-4 flex gap-3">
          <input
            type="text"
            required
            disabled={isLoading}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask AI agent to dispatch plumbers, query lease clauses, or analyze rent metrics..."
            className="flex-1 bg-slate-900 border border-slate-800 rounded-xl py-3 px-4 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-150"
          />
          <button
            type="submit"
            disabled={isLoading}
            className="bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-800 text-white p-3 rounded-xl transition duration-150 flex items-center justify-center shrink-0 shadow-md shadow-indigo-600/10"
          >
            <Send className="h-5 w-5" />
          </button>
        </form>

      </div>
    </Layout>
  );
}
