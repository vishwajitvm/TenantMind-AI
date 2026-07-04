'use client';

import React, { useState } from 'react';
import Layout from '../../components/Layout';
import { useStore, ApprovalRequest } from '../../components/store';
import { CheckSquare, ShieldCheck, Check, X, Clock, HelpCircle, User } from 'lucide-react';

export default function ApprovalsPage() {
  const { approvals, approveRequest, rejectRequest } = useStore();
  const [filter, setFilter] = useState<'all' | 'pending' | 'approved' | 'rejected'>('all');

  const filteredApprovals = approvals.filter(a => {
    if (filter === 'all') return true;
    return a.status === filter;
  });

  return (
    <Layout requiredPermission="approve:actions">
      <div className="space-y-6">
        
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-slate-100">AI Action Authorization Board</h1>
            <p className="text-xs text-slate-400 mt-1">
              Verify and confirm automated MCP tool dispatches, escalating rent limits, or external operations.
            </p>
          </div>
          <div className="flex gap-1 bg-slate-900 border border-slate-800 p-1 rounded-xl">
            {(['all', 'pending', 'approved', 'rejected'] as const).map(f => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`py-1.5 px-3 rounded-lg text-xs font-semibold capitalize transition ${
                  filter === f
                    ? 'bg-indigo-600/10 border-indigo-500 text-indigo-300'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {f}
              </button>
            ))}
          </div>
        </div>

        {/* List of Requests */}
        <div className="space-y-4">
          {filteredApprovals.length === 0 ? (
            <div className="p-12 text-center text-slate-500 border border-dashed border-slate-800 rounded-2xl">
              No approval requests found matching the current criteria.
            </div>
          ) : (
            filteredApprovals.map((appr) => (
              <div
                key={appr.id}
                className={`p-5 rounded-2xl border bg-slate-900/20 flex flex-col md:flex-row md:items-center justify-between gap-4 transition ${
                  appr.status === 'pending'
                    ? 'border-slate-800/80 shadow-md'
                    : 'border-slate-900/60 opacity-75'
                }`}
              >
                <div className="space-y-2 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className={`px-2.5 py-0.5 rounded-full text-[9px] uppercase font-bold border ${
                      appr.status === 'pending'
                        ? 'bg-rose-500/10 border-rose-500/20 text-rose-400'
                        : appr.status === 'approved'
                          ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                          : 'bg-slate-800 border-slate-700 text-slate-400'
                    }`}>
                      {appr.status}
                    </span>
                    <span className="text-[10px] text-slate-500 font-mono">ID: {appr.id}</span>
                  </div>

                  <h3 className="text-sm font-bold text-slate-250">{appr.title}</h3>
                  <p className="text-xs text-slate-400 max-w-2xl">{appr.description}</p>

                  <div className="flex flex-wrap items-center gap-3 pt-1 text-[10px] text-slate-500">
                    <span className="flex items-center gap-1">
                      <Clock className="h-3.5 w-3.5" /> {appr.requestedAt}
                    </span>
                    <span className="flex items-center gap-1">
                      <User className="h-3.5 w-3.5" /> Requested by: {appr.requestedBy}
                    </span>
                    <span className="bg-slate-800 px-2 py-0.5 rounded font-mono text-slate-400">
                      Tool: {appr.tool}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-2 self-start md:self-center shrink-0">
                  {appr.status === 'pending' ? (
                    <>
                      <button
                        onClick={() => approveRequest(appr.id)}
                        className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold py-2 px-4 rounded-xl flex items-center gap-1 transition shadow-md shadow-indigo-600/10"
                      >
                        <Check className="h-4 w-4" /> Approve
                      </button>
                      <button
                        onClick={() => rejectRequest(appr.id)}
                        className="bg-slate-800 hover:bg-slate-700 text-slate-350 text-xs font-bold py-2 px-4 rounded-xl flex items-center gap-1 transition border border-slate-700/80"
                      >
                        <X className="h-4 w-4" /> Reject
                      </button>
                    </>
                  ) : (
                    <div className="flex items-center gap-1 text-xs text-slate-400 font-mono uppercase bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-xl">
                      {appr.status === 'approved' ? (
                        <Check className="h-4 w-4 text-emerald-400" />
                      ) : (
                        <X className="h-4 w-4 text-rose-400" />
                      )}
                      <span>Action {appr.status}</span>
                    </div>
                  )}
                </div>

              </div>
            ))
          )}
        </div>

      </div>
    </Layout>
  );
}
