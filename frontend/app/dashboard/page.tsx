'use client';

import React from 'react';
import Layout from '../../components/Layout';
import { useStore } from '../../components/store';
import { Files, CheckSquare, Cpu, Activity, ArrowUpRight, CheckCircle2, Clock } from 'lucide-react';
import Link from 'next/link';

export default function DashboardPage() {
  const { documents, approvals, mcpTools, auditLogs, selectedTenant } = useStore();

  const tenantDocs = documents.filter(d => d.tenantId === selectedTenant?.id);
  const pendingApprovals = approvals.filter(a => a.status === 'pending');
  const activeTools = mcpTools.filter(t => t.status === 'active');
  const recentLogs = auditLogs.filter(l => l.tenantId === selectedTenant?.id).slice(0, 5);

  const metrics = [
    { name: 'Indexed Documents', value: tenantDocs.length, icon: Files, color: 'text-indigo-400', bg: 'bg-indigo-500/10' },
    { name: 'Pending Approvals', value: pendingApprovals.length, icon: CheckSquare, color: 'text-rose-400', bg: 'bg-rose-500/10' },
    { name: 'Active MCP Tools', value: activeTools.length, icon: Cpu, color: 'text-amber-400', bg: 'bg-amber-500/10' },
    { name: 'System Operations', value: auditLogs.length, icon: Activity, color: 'text-emerald-400', bg: 'bg-emerald-500/10' },
  ];

  return (
    <Layout>
      <div className="space-y-6">
        
        {/* Welcome Banner */}
        <div className="bg-gradient-to-r from-slate-900 via-indigo-950/20 to-slate-900 border border-slate-800 p-6 rounded-2xl flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-slate-100">Welcome to TenantMind Workspace</h1>
            <p className="text-sm text-slate-400 mt-1">
              Active Scope: <span className="text-indigo-400 font-semibold">{selectedTenant?.name}</span> ({selectedTenant?.domain})
            </p>
          </div>
          <Link
            href="/chat"
            className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold px-4 py-2 rounded-xl transition duration-150 flex items-center gap-1 shadow-md shadow-indigo-600/10"
          >
            Start Chat Agent <ArrowUpRight className="h-4 w-4" />
          </Link>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {metrics.map((m) => {
            const Icon = m.icon;
            return (
              <div key={m.name} className="bg-slate-900/40 border border-slate-800/80 p-5 rounded-2xl flex items-center gap-4">
                <div className={`${m.bg} ${m.color} p-3 rounded-xl border border-white/5`}>
                  <Icon className="h-6 w-6" />
                </div>
                <div>
                  <p className="text-xs text-slate-400 font-medium">{m.name}</p>
                  <p className="text-2xl font-extrabold text-slate-100 mt-1">{m.value}</p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Bottom Section */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Recent Audits */}
          <div className="lg:col-span-2 bg-slate-900/30 border border-slate-800/80 rounded-2xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">Tenant Audit Log Activity</h3>
              <Link href="/audit-logs" className="text-xs text-indigo-400 hover:text-indigo-300 font-medium">
                View all logs
              </Link>
            </div>
            
            <div className="divide-y divide-slate-800/60">
              {recentLogs.length === 0 ? (
                <div className="py-6 text-center text-xs text-slate-500">No recent operations in this tenant.</div>
              ) : (
                recentLogs.map((log) => (
                  <div key={log.id} className="py-3 flex items-center justify-between gap-4">
                    <div className="min-w-0">
                      <p className="text-xs font-semibold text-slate-300 truncate">{log.details}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-[10px] text-slate-500 font-mono">{log.timestamp}</span>
                        <span className="text-[10px] bg-slate-800 px-1.5 py-0.5 rounded text-slate-400 font-mono">
                          By: {log.actor}
                        </span>
                      </div>
                    </div>
                    <div>
                      {log.status === 'success' ? (
                        <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] px-2 py-0.5 rounded-full font-bold">
                          Success
                        </span>
                      ) : (
                        <span className="bg-rose-500/10 text-rose-400 border border-rose-500/20 text-[10px] px-2 py-0.5 rounded-full font-bold">
                          Failed
                        </span>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Staged Approvals Quick Panel */}
          <div className="bg-slate-900/30 border border-slate-800/80 rounded-2xl p-5 space-y-4">
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider">Pending Action Gateway</h3>
            
            <div className="space-y-3">
              {pendingApprovals.length === 0 ? (
                <div className="text-center py-8 text-xs text-slate-500 border border-dashed border-slate-800 rounded-xl">
                  All systems operating securely. No outstanding approvals.
                </div>
              ) : (
                pendingApprovals.map((appr) => (
                  <div key={appr.id} className="p-4 border border-rose-500/20 bg-rose-500/5 rounded-xl space-y-3">
                    <div>
                      <h4 className="text-xs font-bold text-slate-200">{appr.title}</h4>
                      <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">{appr.description}</p>
                    </div>
                    <div className="flex items-center justify-between text-[10px] text-slate-500">
                      <span>Tool: {appr.tool}</span>
                      <Link href="/approvals" className="text-rose-400 hover:underline font-bold">
                        Review Staging
                      </Link>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

      </div>
    </Layout>
  );
}
