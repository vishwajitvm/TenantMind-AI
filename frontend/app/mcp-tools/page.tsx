'use client';

import React, { useState } from 'react';
import Layout from '../../components/Layout';
import { useStore, MCPTool } from '../../components/store';
import { Cpu, Plus, ToggleLeft, ToggleRight, Settings, Radio, Globe, ShieldAlert } from 'lucide-react';

export default function MCPToolsPage() {
  const { mcpTools, toggleMCPTool, addMCPTool } = useStore();
  
  // Registration state
  const [newToolName, setNewToolName] = useState('');
  const [newToolDesc, setNewToolDesc] = useState('');
  const [newToolEndpoint, setNewToolEndpoint] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newToolName.trim() || !newToolEndpoint.trim()) return;
    addMCPTool({
      name: newToolName,
      description: newToolDesc,
      endpoint: newToolEndpoint,
      headers: { 'X-Custom-Auth': 'mcp-secret-key-999' }
    });
    setNewToolName('');
    setNewToolDesc('');
    setNewToolEndpoint('');
  };

  return (
    <Layout requiredRole="admin">
      <div className="space-y-6">
        
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-slate-100">Model Context Protocol (MCP) Connectors</h1>
            <p className="text-xs text-slate-400 mt-1">
              Extend LLM capabilities with semantic tool execution, sandboxed parameters, and dynamic routing schemas.
            </p>
          </div>
          <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs px-3 py-1 rounded-full font-bold flex items-center gap-1">
            <Radio className="h-3.5 w-3.5 animate-pulse" /> MCP Gateway: Active
          </span>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          
          {/* Register Tool */}
          <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
              <Plus className="h-4.5 w-4.5 text-indigo-400" /> Register Connector Tool
            </h3>

            <form onSubmit={handleSubmit} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Tool Identifier</label>
                <input
                  type="text"
                  required
                  value={newToolName}
                  onChange={(e) => setNewToolName(e.target.value)}
                  placeholder="e.g. city-rent-index-checker"
                  className="w-full bg-slate-950/80 border border-slate-800 rounded-xl py-2.5 px-3 text-xs text-slate-250 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Description</label>
                <textarea
                  value={newToolDesc}
                  onChange={(e) => setNewToolDesc(e.target.value)}
                  placeholder="Retrieves live municipal rent rules..."
                  rows={3}
                  className="w-full bg-slate-950/80 border border-slate-800 rounded-xl py-2 px-3 text-xs text-slate-250 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition resize-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">HTTP Router Endpoint</label>
                <input
                  type="url"
                  required
                  value={newToolEndpoint}
                  onChange={(e) => setNewToolEndpoint(e.target.value)}
                  placeholder="http://localhost:8000/api/v1/tools/..."
                  className="w-full bg-slate-950/80 border border-slate-800 rounded-xl py-2.5 px-3 text-xs text-slate-250 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
                />
              </div>

              <button
                type="submit"
                className="w-full bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold py-2.5 rounded-xl transition flex items-center justify-center gap-1.5 shadow-md shadow-indigo-600/10"
              >
                <Cpu className="h-4 w-4" /> Mount Protocol Tool
              </button>
            </form>
          </div>

          {/* Connectors Status */}
          <div className="lg:col-span-2 space-y-4">
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">Mounted Connector Registry</h3>
            
            <div className="grid sm:grid-cols-2 gap-4">
              {mcpTools.map((tool) => (
                <div
                  key={tool.id}
                  className={`p-5 rounded-2xl border flex flex-col justify-between min-h-[170px] transition ${
                    tool.status === 'active'
                      ? 'bg-slate-900/30 border-slate-800'
                      : 'bg-slate-950/50 border-slate-900/60 opacity-60'
                  }`}
                >
                  <div className="space-y-2">
                    <div className="flex items-start justify-between">
                      <div className="bg-indigo-600/10 p-2 rounded-xl border border-indigo-500/10 text-indigo-400">
                        <Cpu className="h-5 w-5" />
                      </div>
                      
                      <button
                        onClick={() => toggleMCPTool(tool.id)}
                        className="text-slate-400 hover:text-slate-100 transition"
                        title={tool.status === 'active' ? 'Deactivate tool' : 'Activate tool'}
                      >
                        {tool.status === 'active' ? (
                          <ToggleRight className="h-7 w-7 text-emerald-500" />
                        ) : (
                          <ToggleLeft className="h-7 w-7 text-slate-600" />
                        )}
                      </button>
                    </div>

                    <h4 className="text-sm font-bold text-slate-200">{tool.name}</h4>
                    <p className="text-xs text-slate-400 line-clamp-2">{tool.description}</p>
                  </div>

                  <div className="border-t border-slate-800/80 pt-3 mt-4 flex items-center gap-1 text-[10px] text-slate-500 font-mono truncate">
                    <Globe className="h-3 w-3 text-slate-400" /> {tool.endpoint}
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>
    </Layout>
  );
}
