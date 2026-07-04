import React from 'react';
import { useStore } from './store';
import { Sun, Moon, RefreshCw, Radio } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { darkMode, toggleDarkMode, selectedTenant } = useStore();

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-950/50 backdrop-blur-xl px-6 flex items-center justify-between sticky top-0 z-40">
      <div className="flex items-center gap-3">
        <span className="text-sm font-medium text-slate-400">Context:</span>
        <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 py-1 px-3 rounded-full text-xs text-indigo-300 font-semibold shadow-inner">
          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          {selectedTenant ? selectedTenant.name : 'No Tenant Context'}
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* API Health */}
        <div className="flex items-center gap-1.5 text-xs text-slate-400 bg-slate-900/60 py-1 px-2.5 rounded-lg border border-slate-800/80">
          <Radio className="h-3 w-3 text-emerald-400" />
          <span>Backend Connected</span>
        </div>

        {/* Sync Indicator */}
        <button className="text-slate-400 hover:text-slate-200 p-1.5 rounded-lg hover:bg-slate-900 transition duration-150" title="Sync Keycloak Realms">
          <RefreshCw className="h-4 w-4" />
        </button>

        {/* Dark Mode toggle */}
        <button
          onClick={toggleDarkMode}
          className="text-slate-400 hover:text-amber-400 p-1.5 rounded-lg hover:bg-slate-900 transition duration-150"
          title="Toggle Theme Mode"
        >
          {darkMode ? <Sun className="h-4 w-4 text-amber-400" /> : <Moon className="h-4 w-4 text-slate-400" />}
        </button>
      </div>
    </header>
  );
};
export default Navbar;
