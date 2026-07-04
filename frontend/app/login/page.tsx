'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useStore } from '../../components/store';
import { Shield, Key, Lock, Mail, UserCheck } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const login = useStore(state => state.login);
  const [username, setUsername] = useState('admin_user');
  const [selectedRole, setSelectedRole] = useState<'admin' | 'manager' | 'viewer'>('admin');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    const roles = selectedRole === 'admin' 
      ? ['admin', 'manager'] 
      : selectedRole === 'manager' 
        ? ['manager'] 
        : ['viewer'];
    login(username, roles);
    router.push('/org-selector');
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-950/40 via-slate-950 to-slate-950">
      <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl max-w-md w-full shadow-2xl space-y-6">
        
        {/* Brand */}
        <div className="text-center space-y-2">
          <div className="bg-indigo-600/10 p-3.5 rounded-2xl w-14 h-14 mx-auto flex items-center justify-center border border-indigo-500/20 text-indigo-400">
            <Shield className="h-7 w-7" />
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">TenantMind AI</h1>
          <p className="text-xs text-slate-400">Keycloak Federated IAM Auth Gateway</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">Username</label>
            <div className="relative">
              <Mail className="absolute left-3.5 top-3 h-4.5 w-4.5 text-slate-500" />
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full bg-slate-950/60 border border-slate-800 rounded-xl py-2.5 pl-11 pr-4 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                placeholder="Enter username"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5">Keycloak Security Roles</label>
            <div className="grid grid-cols-3 gap-2.5">
              {(['admin', 'manager', 'viewer'] as const).map(role => (
                <button
                  type="button"
                  key={role}
                  onClick={() => setSelectedRole(role)}
                  className={`py-2 px-3 rounded-xl border text-xs font-semibold uppercase transition flex flex-col items-center justify-center gap-1.5 ${
                    selectedRole === role
                      ? 'bg-indigo-600/15 border-indigo-500 text-indigo-300'
                      : 'bg-slate-950/40 border-slate-800 text-slate-400 hover:bg-slate-900'
                  }`}
                >
                  <UserCheck className="h-4 w-4" />
                  {role}
                </button>
              ))}
            </div>
            <p className="text-[10px] text-slate-500 mt-2">
              * Select 'viewer' to test permission-denied views on admin sections.
            </p>
          </div>

          <button
            type="submit"
            className="w-full bg-gradient-to-r from-indigo-600 to-indigo-800 hover:from-indigo-500 hover:to-indigo-700 text-white font-medium py-3 rounded-xl transition duration-150 shadow-lg shadow-indigo-600/20 flex items-center justify-center gap-2 text-sm"
          >
            <Lock className="h-4 w-4" /> Connect SSO Session
          </button>
        </form>

        <div className="border-t border-slate-800/80 pt-4 text-center">
          <span className="text-[11px] text-slate-500 font-mono">
            Client ID: frontend-client | Realm: tenantmind
          </span>
        </div>

      </div>
    </div>
  );
}
