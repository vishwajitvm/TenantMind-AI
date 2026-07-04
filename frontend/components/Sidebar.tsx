import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useStore } from './store';
import { 
  LayoutDashboard, 
  MessageSquare, 
  Files, 
  Cpu, 
  CheckSquare, 
  History, 
  Settings, 
  LogOut,
  Building,
  Shield,
  Layers
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const pathname = usePathname();
  const { user, tenants, selectedTenant, selectTenant, logout } = useStore();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'AI Chat Agent', href: '/chat', icon: MessageSquare },
    { name: 'Documents', href: '/documents', icon: Files },
    { name: 'MCP Tools', href: '/mcp-tools', icon: Cpu },
    { name: 'Approvals', href: '/approvals', icon: CheckSquare, badge: useStore(state => state.approvals.filter(a => a.status === 'pending').length) },
    { name: 'Audit Logs', href: '/audit-logs', icon: History },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950/80 backdrop-blur-xl flex flex-col h-screen sticky top-0">
      {/* Brand Logo */}
      <div className="p-6 border-b border-slate-800 flex items-center gap-3">
        <div className="bg-indigo-600 p-2 rounded-lg text-white shadow-lg shadow-indigo-500/20">
          <Layers className="h-6 w-6" />
        </div>
        <div>
          <span className="font-bold text-lg text-white tracking-tight">TenantMind <span className="text-indigo-400">AI</span></span>
          <p className="text-xs text-slate-400">Cognitive Multi-Tenant</p>
        </div>
      </div>

      {/* Tenant Selector */}
      <div className="p-4 border-b border-slate-800">
        <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1">
          <Building className="h-3 w-3" /> Active Organization Context
        </label>
        <select
          value={selectedTenant?.id || ''}
          onChange={(e) => selectTenant(e.target.value)}
          className="w-full bg-slate-900 border border-slate-800 rounded-lg py-2 px-3 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-150"
        >
          {tenants.map(t => (
            <option key={t.id} value={t.id}>
              {t.name} ({t.plan})
            </option>
          ))}
        </select>
        <p className="text-[10px] text-indigo-400/80 mt-1.5 italic font-mono truncate">
          Header: X-Tenant-ID: {selectedTenant?.id || 'none'}
        </p>
      </div>

      {/* Main Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
        {navigation.map((item) => {
          const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname?.startsWith(item.href));
          const Icon = item.icon;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center justify-between px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 group ${
                isActive
                  ? 'bg-gradient-to-r from-indigo-600 to-indigo-800 text-white shadow-lg shadow-indigo-600/10'
                  : 'text-slate-400 hover:bg-slate-900 hover:text-slate-100'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`h-5 w-5 ${isActive ? 'text-white' : 'text-slate-400 group-hover:text-indigo-400'}`} />
                <span>{item.name}</span>
              </div>
              {item.badge && item.badge > 0 ? (
                <span className={`px-2 py-0.5 text-xs rounded-full ${isActive ? 'bg-white text-indigo-800 font-bold' : 'bg-rose-500/20 text-rose-400 font-semibold border border-rose-500/30'}`}>
                  {item.badge}
                </span>
              ) : null}
            </Link>
          );
        })}
      </nav>

      {/* User Information */}
      <div className="p-4 border-t border-slate-800 bg-slate-900/30">
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-tr from-indigo-500 to-purple-600 h-10 w-10 rounded-full flex items-center justify-center text-white font-bold shadow-md">
            {user?.username.charAt(0).toUpperCase() || 'U'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-slate-200 truncate">{user?.username || 'Guest'}</p>
            <div className="flex items-center gap-1 mt-0.5">
              <Shield className="h-3 w-3 text-indigo-400" />
              <span className="text-[10px] text-slate-400 uppercase font-bold truncate">
                {user?.roles.join(', ') || 'No Role'}
              </span>
            </div>
          </div>
          <button
            onClick={logout}
            className="text-slate-400 hover:text-rose-400 p-1.5 rounded-lg hover:bg-rose-500/10 transition"
            title="Logout"
          >
            <LogOut className="h-5 w-5" />
          </button>
        </div>
      </div>
    </aside>
  );
};
export default Sidebar;
