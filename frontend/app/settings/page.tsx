'use client';

import React from 'react';
import Layout from '../../components/Layout';
import { useStore } from '../../components/store';
import { Settings, Shield, User, Sliders, AlertTriangle } from 'lucide-react';

export default function SettingsPage() {
  const { selectedTenant, user } = useStore();

  return (
    <Layout>
      <div className="space-y-6">
        
        <div>
          <h1 className="text-xl font-bold text-slate-100">Global System Parameters</h1>
          <p className="text-xs text-slate-400 mt-1">
            Configure integration clients, security credentials, and cognitive assistant thresholds.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          
          {/* User Profile & Keycloak Scopes */}
          <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
              <User className="h-4.5 w-4.5 text-indigo-400" /> Identity Provider Profile
            </h3>

            <div className="space-y-3.5 text-xs">
              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold block">Assigned SSO Username</span>
                <span className="text-slate-200 font-semibold">{user?.username}</span>
              </div>

              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold block">Email Address</span>
                <span className="text-slate-200 font-semibold">{user?.email}</span>
              </div>

              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold block">Keycloak IAM Roles</span>
                <div className="flex flex-wrap gap-1.5 mt-1">
                  {user?.roles.map(r => (
                    <span key={r} className="bg-indigo-600/10 border border-indigo-500/20 text-indigo-400 px-2.5 py-0.5 rounded text-[10px] uppercase font-bold">
                      {r}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold block">Permitted OpenID Scopes</span>
                <div className="flex flex-wrap gap-1.5 mt-1">
                  {user?.permissions.map(p => (
                    <span key={p} className="bg-slate-900 border border-slate-800 text-slate-400 px-2 py-0.5 rounded font-mono text-[9px]">
                      {p}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* IAM Configuration */}
          <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
              <Shield className="h-4.5 w-4.5 text-indigo-400" /> Keycloak SSO Configuration
            </h3>

            <div className="space-y-3 text-xs">
              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold block">SSO Target Host</span>
                <span className="font-mono text-slate-300">
                  {process.env.NEXT_PUBLIC_KEYCLOAK_URL || 'http://localhost:8080'}
                </span>
              </div>

              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold block">Security Realm ID</span>
                <span className="font-mono text-slate-350">
                  {process.env.NEXT_PUBLIC_KEYCLOAK_REALM || 'tenantmind'}
                </span>
              </div>

              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold block">Registered Client ID</span>
                <span className="font-mono text-slate-350">
                  {process.env.NEXT_PUBLIC_KEYCLOAK_CLIENT_ID || 'frontend-client'}
                </span>
              </div>
            </div>
          </div>

          {/* Tenant Parameters */}
          <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
              <Sliders className="h-4.5 w-4.5 text-indigo-400" /> Tenant Operations Schema
            </h3>

            <div className="space-y-3.5 text-xs">
              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold block">Active Tenant Context</span>
                <span className="font-bold text-slate-205">{selectedTenant?.name}</span>
              </div>

              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold block">Domain Scope Restriction</span>
                <span className="font-mono text-slate-350">{selectedTenant?.domain}</span>
              </div>

              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold block">Subscription Tier</span>
                <span className="text-indigo-400 font-bold uppercase">{selectedTenant?.plan}</span>
              </div>
            </div>
          </div>

          {/* Danger Zone */}
          <div className="border border-rose-500/20 bg-rose-500/5 p-5 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
              <AlertTriangle className="h-4.5 w-4.5" /> Security System Override
            </h3>

            <p className="text-xs text-slate-400">
              Permanently clear local cached OpenID tokens, organization indexes, and context tokens. This action is irreversible.
            </p>

            <button className="bg-rose-500 hover:bg-rose-600 text-white text-xs font-bold py-2.5 px-4 rounded-xl transition shadow-md shadow-rose-600/10">
              Clear Indexed Context
            </button>
          </div>

        </div>

      </div>
    </Layout>
  );
}
