'use client';

import React, { useState } from 'react';
import Layout from '../../components/Layout';
import { useStore } from '../../components/store';
import { History, Search, ShieldCheck, Terminal, Filter } from 'lucide-react';

export default function AuditLogsPage() {
  const { auditLogs, selectedTenant } = useStore();
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'success' | 'failed'>('all');

  const tenantLogs = auditLogs.filter(log => log.tenantId === selectedTenant?.id);

  const filteredLogs = tenantLogs.filter(log => {
    const matchesSearch = log.details.toLowerCase().includes(search.toLowerCase()) || 
                          log.actor.toLowerCase().includes(search.toLowerCase()) ||
                          log.action.toLowerCase().includes(search.toLowerCase());
    const matchesStatus = statusFilter === 'all' || log.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <Layout>
      <div className="space-y-6">
        
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-xl font-bold text-slate-100">Immutable Audit Trail</h1>
            <p className="text-xs text-slate-400 mt-1">
              Tracks actions, system-triggered events, and Keycloak permission verification checks.
            </p>
          </div>

          <div className="flex items-center gap-2 bg-slate-900/60 border border-slate-800 p-1.5 rounded-xl shrink-0">
            <Terminal className="h-4 w-4 text-indigo-400 shrink-0 ml-1.5" />
            <span className="text-[11px] text-slate-400 font-mono">Scope: X-Tenant-ID={selectedTenant?.id}</span>
          </div>
        </div>

        {/* Filter Controls */}
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-2.5 h-4.5 w-4.5 text-slate-500" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search audit trail by actor, action or event logs..."
              className="w-full bg-slate-900 border border-slate-800 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-205 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
            />
          </div>

          <div className="flex items-center gap-1.5 shrink-0 bg-slate-900 border border-slate-800 p-1.5 rounded-xl">
            <Filter className="h-4.5 w-4.5 text-slate-500 ml-1" />
            {(['all', 'success', 'failed'] as const).map(status => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={`py-1 px-2.5 rounded-lg text-xs font-semibold capitalize transition ${
                  statusFilter === status
                    ? 'bg-indigo-600/10 border border-indigo-500/20 text-indigo-300'
                    : 'text-slate-450 hover:text-slate-200'
                }`}
              >
                {status}
              </button>
            ))}
          </div>
        </div>

        {/* Log Viewer */}
        <div className="bg-slate-900/20 border border-slate-800 rounded-2xl overflow-hidden shadow-inner">
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-left text-xs">
              <thead>
                <tr className="bg-slate-950/60 border-b border-slate-800 text-slate-400 font-bold uppercase tracking-wider">
                  <th className="p-4">Timestamp</th>
                  <th className="p-4">Actor</th>
                  <th className="p-4">Action Event</th>
                  <th className="p-4">Details</th>
                  <th className="p-4">IP Address</th>
                  <th className="p-4 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                {filteredLogs.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="p-8 text-center text-slate-500 font-sans">
                      No matching audit event trails found.
                    </td>
                  </tr>
                ) : (
                  filteredLogs.map((log) => (
                    <tr key={log.id} className="hover:bg-slate-900/10 transition">
                      <td className="p-4 text-slate-400 whitespace-nowrap">{log.timestamp}</td>
                      <td className="p-4 font-semibold text-slate-200">{log.actor}</td>
                      <td className="p-4 text-indigo-400 font-semibold whitespace-nowrap">{log.action}</td>
                      <td className="p-4 text-slate-300 max-w-sm truncate" title={log.details}>
                        {log.details}
                      </td>
                      <td className="p-4 text-slate-500">{log.ipAddress}</td>
                      <td className="p-4 text-right">
                        <span className={`inline-flex px-2 py-0.5 rounded text-[9px] uppercase font-bold border ${
                          log.status === 'success'
                            ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                            : 'bg-rose-500/10 border-rose-500/20 text-rose-400'
                        }`}>
                          {log.status}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </Layout>
  );
}
