import { create } from 'zustand';

export interface User {
  username: string;
  email: string;
  roles: string[];
  permissions: string[];
}

export interface Tenant {
  id: string;
  name: string;
  domain: string;
  plan: 'Growth' | 'Enterprise' | 'Free';
}

export interface DocumentFile {
  id: string;
  name: string;
  size: string;
  uploadedAt: string;
  status: 'processing' | 'indexed' | 'failed';
  tokens: number;
  tenantId: string;
  uploader: string;
  category: string;
}

export interface FlowNode {
  id: string;
  type: string;
  data: { label: string; [key: string]: any };
  position: { x: number; y: number };
}

export interface FlowEdge {
  id: string;
  source: string;
  target: string;
  animated?: boolean;
}

export interface ApprovalRequest {
  id: string;
  title: string;
  description: string;
  tool: string;
  params: Record<string, any>;
  status: 'pending' | 'approved' | 'rejected';
  requestedAt: string;
  requestedBy: string;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  content: string;
  timestamp: string;
  citations?: { id: string; docName: string; snippet: string; score: number }[];
  flowData?: {
    nodes: FlowNode[];
    edges: FlowEdge[];
  };
  approvalId?: string;
  pendingExecution?: boolean;
}

export interface MCPTool {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'inactive';
  endpoint: string;
  headers: Record<string, string>;
  lastCalled?: string;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  actor: string;
  action: string;
  tenantId: string;
  details: string;
  ipAddress: string;
  status: 'success' | 'failed';
}

interface State {
  user: User | null;
  isAuthenticated: boolean;
  selectedTenant: Tenant | null;
  tenants: Tenant[];
  documents: DocumentFile[];
  chatHistory: ChatMessage[];
  mcpTools: MCPTool[];
  approvals: ApprovalRequest[];
  auditLogs: AuditLog[];
  darkMode: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (username: string, roles: string[]) => void;
  logout: () => void;
  selectTenant: (tenantId: string) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  uploadDocument: (doc: Omit<DocumentFile, 'id' | 'uploadedAt' | 'tokens' | 'status'>) => void;
  deleteDocument: (id: string) => void;
  sendChatMessage: (content: string) => void;
  approveRequest: (id: string) => void;
  rejectRequest: (id: string) => void;
  toggleMCPTool: (id: string) => void;
  addMCPTool: (tool: Omit<MCPTool, 'id' | 'status'>) => void;
  toggleDarkMode: () => void;
  addAuditLog: (log: Omit<AuditLog, 'id' | 'timestamp'>) => void;
}

export const useStore = create<State>((set, get) => ({
  user: {
    username: 'admin_user',
    email: 'admin@tenantmind.ai',
    roles: ['admin', 'manager'],
    permissions: ['read:all', 'write:all', 'execute:tools', 'approve:actions']
  },
  isAuthenticated: true,
  selectedTenant: { id: 'tenant-alpha', name: 'Alpha Properties', domain: 'alpha.tenantmind.ai', plan: 'Enterprise' },
  tenants: [
    { id: 'tenant-alpha', name: 'Alpha Properties', domain: 'alpha.tenantmind.ai', plan: 'Enterprise' },
    { id: 'tenant-beta', name: 'Beta Living Spaces', domain: 'beta.tenantmind.ai', plan: 'Growth' },
    { id: 'tenant-gamma', name: 'Gamma Commercial', domain: 'gamma.tenantmind.ai', plan: 'Free' }
  ],
  documents: [
    { id: 'doc-1', name: 'Lease_Agreement_Alpha_2026.pdf', size: '2.4 MB', uploadedAt: '2026-07-01 10:14', status: 'indexed', tokens: 14500, tenantId: 'tenant-alpha', uploader: 'admin_user', category: 'Leases' },
    { id: 'doc-2', name: 'Maintenance_Log_Q2.xlsx', size: '1.8 MB', uploadedAt: '2026-07-02 14:22', status: 'indexed', tokens: 8200, tenantId: 'tenant-alpha', uploader: 'admin_user', category: 'Maintenance' },
    { id: 'doc-3', name: 'Tenant_Handbook_Draft.docx', size: '4.1 MB', uploadedAt: '2026-07-03 09:05', status: 'processing', tokens: 0, tenantId: 'tenant-alpha', uploader: 'manager_user', category: 'Compliance' },
    { id: 'doc-4', name: 'Beta_Standard_Lease.pdf', size: '3.1 MB', uploadedAt: '2026-07-02 11:30', status: 'indexed', tokens: 12000, tenantId: 'tenant-beta', uploader: 'beta_admin', category: 'Leases' }
  ],
  chatHistory: [
    {
      id: 'msg-1',
      sender: 'assistant',
      content: 'Hello! I am TenantMind AI, your multi-tenant cognitive assistant. How can I help you manage documents, query property logs, or trigger workflows today?',
      timestamp: '09:00 AM'
    }
  ],
  mcpTools: [
    { id: 'tool-lease-analyzer', name: 'Lease Rent Auditor', description: 'Cross-checks lease agreement clauses against local city Rent Control policies.', status: 'active', endpoint: 'http://localhost:8000/api/v1/tools/lease-audit', headers: {} },
    { id: 'tool-maintenance-trigger', name: 'Dispatch Maintenance Dispatcher', description: 'Automatically alerts plumbers, electricians, or handymen via external API integrations.', status: 'active', endpoint: 'http://localhost:8000/api/v1/tools/dispatch', headers: {} },
    { id: 'tool-tenant-portal-sync', name: 'Tenant Portal Sync', description: 'Syncs indexed documents, notification status, and lease parameters to Tenant Portal app.', status: 'inactive', endpoint: 'http://localhost:8000/api/v1/tools/portal-sync', headers: {} }
  ],
  approvals: [
    { id: 'appr-1', title: 'Schedule Main Water Line Repair', description: 'Dispatch service provider "SuperPlumbers" for emergency main line inspection. Estimated cost: $450.', tool: 'Dispatch Maintenance Dispatcher', params: { vendor: 'SuperPlumbers', urgency: 'high', costLimit: 450 }, status: 'pending', requestedAt: '2026-07-04 09:30', requestedBy: 'AI Agent (Automated Workflow)' },
    { id: 'appr-2', title: 'Update Rent Adjustment for Tenant A-10', description: 'Apply 3% escalation index based on city rent indexing standards.', tool: 'Lease Rent Auditor', params: { tenantId: 'A-10', currentRent: 2200, escalation: 0.03 }, status: 'approved', requestedAt: '2026-07-03 16:45', requestedBy: 'AI Agent (Automated Workflow)' }
  ],
  auditLogs: [
    { id: 'log-1', timestamp: '2026-07-04 09:30:12', actor: 'AI Agent', action: 'Requested Action Approval', tenantId: 'tenant-alpha', details: 'Triggered approval request for water line repair dispatch.', ipAddress: 'System-Local', status: 'success' },
    { id: 'log-2', timestamp: '2026-07-04 09:05:44', actor: 'admin_user', action: 'Selected Tenant Tenant-Alpha', tenantId: 'tenant-alpha', details: 'Switched context to Alpha Properties.', ipAddress: '192.168.1.42', status: 'success' },
    { id: 'log-3', timestamp: '2026-07-03 16:47:10', actor: 'admin_user', action: 'Approved Action', tenantId: 'tenant-alpha', details: 'Approved escalation for Rent escalation index for tenant A-10.', ipAddress: '192.168.1.42', status: 'success' }
  ],
  darkMode: true,
  isLoading: false,
  error: null,

  login: (username, roles) => {
    set({
      user: {
        username,
        email: `${username}@tenantmind.ai`,
        roles,
        permissions: roles.includes('admin') ? ['read:all', 'write:all', 'execute:tools', 'approve:actions'] : ['read:all']
      },
      isAuthenticated: true
    });
    get().addAuditLog({
      actor: username,
      action: 'Login',
      tenantId: get().selectedTenant?.id || 'none',
      details: `User logged in with roles: ${roles.join(', ')}`,
      ipAddress: '127.0.0.1',
      status: 'success'
    });
  },

  logout: () => {
    set({ user: null, isAuthenticated: false, selectedTenant: null });
  },

  selectTenant: (tenantId) => {
    const tenant = get().tenants.find(t => t.id === tenantId) || null;
    set({ selectedTenant: tenant });
    if (tenant) {
      get().addAuditLog({
        actor: get().user?.username || 'anonymous',
        action: 'Tenant Switch',
        tenantId: tenantId,
        details: `Switched view context to ${tenant.name}`,
        ipAddress: '127.0.0.1',
        status: 'success'
      });
    }
  },

  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),

  uploadDocument: (doc) => {
    const newDoc: DocumentFile = {
      ...doc,
      id: `doc-${Date.now()}`,
      uploadedAt: new Date().toISOString().replace('T', ' ').substring(0, 16),
      tokens: Math.floor(Math.random() * 8000) + 1000,
      status: 'processing'
    };
    set(state => ({
      documents: [newDoc, ...state.documents]
    }));
    get().addAuditLog({
      actor: get().user?.username || 'anonymous',
      action: 'Document Upload',
      tenantId: doc.tenantId,
      details: `Uploaded document: ${doc.name}`,
      ipAddress: '127.0.0.1',
      status: 'success'
    });

    // Simulate completion
    setTimeout(() => {
      set(state => ({
        documents: state.documents.map(d => d.id === newDoc.id ? { ...d, status: 'indexed' } : d)
      }));
    }, 4000);
  },

  deleteDocument: (id) => {
    const doc = get().documents.find(d => d.id === id);
    set(state => ({
      documents: state.documents.filter(d => d.id !== id)
    }));
    if (doc) {
      get().addAuditLog({
        actor: get().user?.username || 'anonymous',
        action: 'Document Delete',
        tenantId: doc.tenantId,
        details: `Deleted document: ${doc.name}`,
        ipAddress: '127.0.0.1',
        status: 'success'
      });
    }
  },

  sendChatMessage: (content) => {
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}-user`,
      sender: 'user',
      content,
      timestamp: timeStr
    };

    set(state => ({
      chatHistory: [...state.chatHistory, userMsg],
      isLoading: true
    }));

    // Trigger a cool tool execution workflow simulation
    setTimeout(() => {
      let responseContent = `I have received your request regarding "${content}". `;
      let citations;
      let flowData;
      let approvalId;

      if (content.toLowerCase().includes('water') || content.toLowerCase().includes('repair') || content.toLowerCase().includes('plumb')) {
        // Setup React Flow workflow for dispatching maintenance
        const apprId = `appr-${Date.now()}`;
        responseContent += `I detected a maintenance emergency. I queried the tenant lease agreement and found that main line repairs are the landlord's responsibility. I have staged a workflow to dispatch SuperPlumbers. This action requires your approval.`;
        
        citations = [
          { id: 'cit-1', docName: 'Lease_Agreement_Alpha_2026.pdf', snippet: 'Section 14.2: Major Plumbing & Main Utilities repairs shall be borne solely by the landlord...', score: 0.94 }
        ];

        flowData = {
          nodes: [
            { id: '1', type: 'input', data: { label: 'User Query' }, position: { x: 50, y: 100 } },
            { id: '2', type: 'default', data: { label: 'RAG Lease Audit' }, position: { x: 250, y: 100 } },
            { id: '3', type: 'default', data: { label: 'Select Vendor' }, position: { x: 450, y: 100 } },
            { id: '4', type: 'output', data: { label: 'Require Approval' }, position: { x: 650, y: 100 } }
          ],
          edges: [
            { id: 'e1-2', source: '1', target: '2', animated: true },
            { id: 'e2-3', source: '2', target: '3', animated: true },
            { id: 'e3-4', source: '3', target: '4', animated: true }
          ]
        };

        approvalId = apprId;

        // Add staged approval
        set(state => ({
          approvals: [
            {
              id: apprId,
              title: `Dispatch Urgent Repair: ${content}`,
              description: `Emergency maintenance request: "${content}". Automatically selects highest rated plumber under $500.`,
              tool: 'Dispatch Maintenance Dispatcher',
              params: { query: content, limit: 500 },
              status: 'pending',
              requestedAt: new Date().toISOString().replace('T', ' ').substring(0, 16),
              requestedBy: 'AI Agent'
            },
            ...state.approvals
          ]
        }));

      } else if (content.toLowerCase().includes('rent') || content.toLowerCase().includes('lease') || content.toLowerCase().includes('escalation')) {
        responseContent += `Running lease clause audit against the standard city escalation guidelines. Here is the generated execution pipeline:`;
        
        citations = [
          { id: 'cit-2', docName: 'Lease_Agreement_Alpha_2026.pdf', snippet: 'Section 4.1: Annual rent increase shall be pegged to local index, not exceeding 4.5%...', score: 0.88 }
        ];

        flowData = {
          nodes: [
            { id: 'n1', type: 'input', data: { label: 'Query RAG' }, position: { x: 100, y: 50 } },
            { id: 'n2', type: 'default', data: { label: 'Extract Rent Escalation Rules' }, position: { x: 100, y: 150 } },
            { id: 'n3', type: 'output', data: { label: 'Audited Status: Approved' }, position: { x: 100, y: 250 } }
          ],
          edges: [
            { id: 'en1-2', source: 'n1', target: 'n2', animated: true },
            { id: 'en2-3', source: 'n2', target: 'n3', animated: false }
          ]
        };

      } else {
        responseContent += `I scanned the documents in the selected tenant space but could not find a specialized MCP workflow. Executing LLM fallback answer using the context:`;
        citations = [
          { id: 'cit-3', docName: 'Maintenance_Log_Q2.xlsx', snippet: 'Row 32: General building inspections performed by tenant coordinator...', score: 0.65 }
        ];
      }

      const botMsg: ChatMessage = {
        id: `msg-${Date.now()}-bot`,
        sender: 'assistant',
        content: responseContent,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        citations,
        flowData,
        approvalId
      };

      set(state => ({
        chatHistory: [...state.chatHistory, botMsg],
        isLoading: false
      }));

      get().addAuditLog({
        actor: 'AI Agent',
        action: 'Execute Chat Response',
        tenantId: get().selectedTenant?.id || 'none',
        details: `Responded to: ${content.substring(0, 30)}...`,
        ipAddress: 'System-Local',
        status: 'success'
      });

    }, 1500);
  },

  approveRequest: (id) => {
    set(state => ({
      approvals: state.approvals.map(a => a.id === id ? { ...a, status: 'approved' } : a)
    }));
    const req = get().approvals.find(a => a.id === id);
    get().addAuditLog({
      actor: get().user?.username || 'admin',
      action: 'Approve Request',
      tenantId: get().selectedTenant?.id || 'none',
      details: `Approved request: ${req?.title || id}`,
      ipAddress: '127.0.0.1',
      status: 'success'
    });
  },

  rejectRequest: (id) => {
    set(state => ({
      approvals: state.approvals.map(a => a.id === id ? { ...a, status: 'rejected' } : a)
    }));
    const req = get().approvals.find(a => a.id === id);
    get().addAuditLog({
      actor: get().user?.username || 'admin',
      action: 'Reject Request',
      tenantId: get().selectedTenant?.id || 'none',
      details: `Rejected request: ${req?.title || id}`,
      ipAddress: '127.0.0.1',
      status: 'failed'
    });
  },

  toggleMCPTool: (id) => {
    set(state => ({
      mcpTools: state.mcpTools.map(t => t.id === id ? { ...t, status: t.status === 'active' ? 'inactive' : 'active' } : t)
    }));
    const tool = get().mcpTools.find(t => t.id === id);
    get().addAuditLog({
      actor: get().user?.username || 'admin',
      action: 'Toggle MCP Tool',
      tenantId: get().selectedTenant?.id || 'none',
      details: `Toggled ${tool?.name} to ${tool?.status === 'active' ? 'inactive' : 'active'}`,
      ipAddress: '127.0.0.1',
      status: 'success'
    });
  },

  addMCPTool: (tool) => {
    const newTool: MCPTool = {
      ...tool,
      id: `tool-${Date.now()}`,
      status: 'active'
    };
    set(state => ({
      mcpTools: [...state.mcpTools, newTool]
    }));
    get().addAuditLog({
      actor: get().user?.username || 'admin',
      action: 'Add MCP Tool',
      tenantId: get().selectedTenant?.id || 'none',
      details: `Registered tool: ${tool.name}`,
      ipAddress: '127.0.0.1',
      status: 'success'
    });
  },

  toggleDarkMode: () => {
    set(state => ({ darkMode: !state.darkMode }));
  },

  addAuditLog: (log) => {
    const newLog: AuditLog = {
      ...log,
      id: `log-${Date.now()}`,
      timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
    };
    set(state => ({
      auditLogs: [newLog, ...state.auditLogs]
    }));
  }
}));
