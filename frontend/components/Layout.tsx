import React from 'react';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import { useStore } from './store';
import { AlertCircle, ShieldAlert, Loader2 } from 'lucide-react';
import { KeycloakProvider, useKeycloak } from './KeycloakProvider';

interface LayoutContentProps {
  children: React.ReactNode;
  requiredPermission?: string;
  requiredRole?: string;
}

const LayoutContent: React.FC<LayoutContentProps> = ({ children, requiredPermission, requiredRole }) => {
  const { isLoading, error, setError, selectedTenant } = useStore();
  const { hasRole, hasPermission, authenticated } = useKeycloak();

  // 1. Authentication State Guard
  if (!authenticated) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-6 text-center">
        <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl max-w-md w-full shadow-2xl space-y-6">
          <div className="bg-rose-500/10 p-4 rounded-full w-16 h-16 mx-auto flex items-center justify-center border border-rose-500/20">
            <ShieldAlert className="h-8 w-8 text-rose-500" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-100">Session Expired or Unauthorized</h1>
            <p className="text-sm text-slate-400 mt-2">
              Keycloak authentication is required to access TenantMind AI. Please sign in to establish a session.
            </p>
          </div>
          <button
            onClick={() => window.location.reload()}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 rounded-xl transition duration-150 shadow-lg shadow-indigo-600/20"
          >
            Authenticate via Keycloak
          </button>
        </div>
      </div>
    );
  }

  // 2. Organization / Tenant Selection Guard
  if (!selectedTenant) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8 bg-slate-950 min-h-screen">
        <div className="max-w-md text-center space-y-4">
          <div className="mx-auto w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center">
            <AlertCircle className="h-6 w-6 text-amber-500" />
          </div>
          <h2 className="text-lg font-semibold text-slate-100">No Active Tenant Context</h2>
          <p className="text-sm text-slate-400">
            Please select an organization tenant context from the sidebar dropdown to view system assets and logs.
          </p>
        </div>
      </div>
    );
  }

  // 3. Permission & Role Guards
  if (requiredRole && !hasRole(requiredRole)) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8 bg-slate-950/80 min-h-[calc(100vh-4rem)]">
        <div className="max-w-md text-center space-y-4 border border-rose-500/20 bg-rose-500/5 p-6 rounded-2xl">
          <div className="mx-auto w-12 h-12 rounded-xl bg-rose-500/10 flex items-center justify-center border border-rose-500/35">
            <ShieldAlert className="h-6 w-6 text-rose-500" />
          </div>
          <h2 className="text-lg font-semibold text-rose-400">Access Denied: Role Required</h2>
          <p className="text-sm text-slate-400">
            Your current Keycloak identity lacks the necessary <code className="bg-slate-900 px-2 py-1 rounded text-rose-300 font-mono text-xs">{requiredRole}</code> role required to access this resource.
          </p>
        </div>
      </div>
    );
  }

  if (requiredPermission && !hasPermission(requiredPermission)) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8 bg-slate-950/80 min-h-[calc(100vh-4rem)]">
        <div className="max-w-md text-center space-y-4 border border-rose-500/20 bg-rose-500/5 p-6 rounded-2xl">
          <div className="mx-auto w-12 h-12 rounded-xl bg-rose-500/10 flex items-center justify-center border border-rose-500/35">
            <ShieldAlert className="h-6 w-6 text-rose-500" />
          </div>
          <h2 className="text-lg font-semibold text-rose-400">Access Denied: Insufficient Scopes</h2>
          <p className="text-sm text-slate-400">
            This module requires the <code className="bg-slate-900 px-2 py-1 rounded text-rose-300 font-mono text-xs">{requiredPermission}</code> scope validation.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col min-h-screen bg-slate-950 text-slate-100">
      <Navbar />
      <main className="flex-1 p-6 relative">
        {/* Loading Overlay */}
        {isLoading && (
          <div className="absolute inset-0 bg-slate-950/60 backdrop-blur-sm z-50 flex items-center justify-center">
            <div className="flex flex-col items-center gap-3">
              <Loader2 className="h-8 w-8 text-indigo-500 animate-spin" />
              <span className="text-sm font-medium text-slate-400">Processing background task...</span>
            </div>
          </div>
        )}

        {/* Global/API Error State Banner */}
        {error ? (
          <div className="border border-rose-500/20 bg-rose-950/20 p-4 rounded-xl mb-6 flex items-start justify-between gap-3 animate-in fade-in slide-in-from-top-4 duration-300">
            <div className="flex gap-3">
              <AlertCircle className="h-5 w-5 text-rose-400 shrink-0 mt-0.5" />
              <div>
                <h4 className="text-sm font-bold text-rose-400">An Error Occurred</h4>
                <p className="text-xs text-rose-200 mt-1">{error}</p>
              </div>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-xs font-semibold text-rose-400 hover:text-rose-300 hover:underline shrink-0"
            >
              Dismiss
            </button>
          </div>
        ) : null}

        {children}
      </main>
    </div>
  );
};

interface LayoutProps {
  children: React.ReactNode;
  requiredPermission?: string;
  requiredRole?: string;
}

export const Layout: React.FC<LayoutProps> = (props) => {
  return (
    <KeycloakProvider>
      <div className="flex min-h-screen bg-slate-950 text-slate-100 font-sans">
        <Sidebar />
        <LayoutContent {...props} />
      </div>
    </KeycloakProvider>
  );
};
export default Layout;
