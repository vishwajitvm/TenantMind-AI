'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useStore } from '../../components/store';
import { Building, ArrowRight, ShieldCheck, Zap } from 'lucide-react';

export default function OrgSelectorPage() {
  const router = useRouter();
  const { tenants, selectTenant, selectedTenant } = useStore();

  const handleSelect = (id: string) => {
    selectTenant(id);
    router.push('/dashboard');
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-950/40 via-slate-950 to-slate-950">
      <div className="max-w-2xl w-full space-y-6">
        
        {/* Title */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-extrabold text-white tracking-tight">Select Tenant Context</h1>
          <p className="text-sm text-slate-400">
            TenantMind AI automatically sets the dynamic <code className="bg-slate-900 text-indigo-400 font-mono px-1.5 py-0.5 rounded text-xs">X-Tenant-ID</code> header based on your selection.
          </p>
        </div>

        {/* Grid */}
        <div className="grid md:grid-cols-3 gap-4">
          {tenants.map(t => {
            const isSelected = selectedTenant?.id === t.id;
            return (
              <div
                key={t.id}
                onClick={() => handleSelect(t.id)}
                className={`group relative p-6 rounded-2xl border text-left cursor-pointer transition-all duration-300 flex flex-col justify-between min-h-[160px] ${
                  isSelected
                    ? 'bg-indigo-950/20 border-indigo-500 shadow-lg shadow-indigo-600/10'
                    : 'bg-slate-900/40 border-slate-800/80 hover:border-slate-700 hover:bg-slate-900/60'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between">
                    <div className={`p-2 rounded-xl border ${isSelected ? 'bg-indigo-600/10 border-indigo-500/30 text-indigo-400' : 'bg-slate-950 border-slate-800 text-slate-400'}`}>
                      <Building className="h-5 w-5" />
                    </div>
                    {t.plan === 'Enterprise' && (
                      <span className="flex items-center gap-0.5 bg-amber-500/10 border border-amber-500/20 text-[9px] text-amber-400 font-extrabold px-1.5 py-0.5 rounded-full uppercase tracking-wider">
                        <Zap className="h-2 w-2 fill-amber-400" /> Premium
                      </span>
                    )}
                  </div>
                  <h3 className="text-sm font-semibold text-slate-200 mt-4 group-hover:text-white transition">
                    {t.name}
                  </h3>
                  <p className="text-xs text-slate-400 mt-1 font-mono">{t.domain}</p>
                </div>

                <div className="flex items-center justify-between mt-4">
                  <span className="text-[10px] font-mono text-slate-500">ID: {t.id}</span>
                  <span className="text-xs font-semibold text-indigo-400 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all duration-200">
                    Enter <ArrowRight className="h-3.5 w-3.5" />
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Back Link */}
        <div className="text-center">
          <p className="text-xs text-slate-500">
            Don't see your organization? Contact your Keycloak Tenant Admin.
          </p>
        </div>

      </div>
    </div>
  );
}
