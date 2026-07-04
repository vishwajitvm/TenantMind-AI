import { useStore } from '../components/store';

describe('TenantMind AI Pages & Workflows Test Suite', () => {
  beforeEach(() => {
    // Reset Zustand store state before each test
    useStore.setState({
      user: {
        username: 'admin_user',
        email: 'admin@tenantmind.ai',
        roles: ['admin', 'manager'],
        permissions: ['read:all', 'write:all', 'execute:tools', 'approve:actions']
      },
      isAuthenticated: true,
      selectedTenant: { id: 'tenant-alpha', name: 'Alpha Properties', domain: 'alpha.tenantmind.ai', plan: 'Enterprise' },
      chatHistory: [
        {
          id: 'msg-1',
          sender: 'assistant',
          content: 'Hello! I am TenantMind AI, your multi-tenant cognitive assistant.',
          timestamp: '09:00 AM'
        }
      ],
      mcpTools: [
        { id: 'tool-lease-analyzer', name: 'Lease Rent Auditor', description: 'Audits lease agreements.', status: 'active', endpoint: 'http://localhost:8000/api/v1/tools/lease-audit', headers: {} }
      ],
      approvals: [
        { id: 'appr-1', title: 'Schedule Main Water Line Repair', description: 'Urgent plumbing.', tool: 'Dispatch Maintenance Dispatcher', params: {}, status: 'pending', requestedAt: '2026-07-04 09:30', requestedBy: 'AI Agent' }
      ],
      auditLogs: []
    });
  });

  // 1. Organization selector tests
  test('OrgSelector: switching tenant updates context and adds audit log', () => {
    const store = useStore.getState();
    expect(store.selectedTenant?.id).toBe('tenant-alpha');

    // Switch context
    store.selectTenant('tenant-beta');
    const state = useStore.getState();
    expect(state.selectedTenant?.id).toBe('tenant-beta');
    expect(state.selectedTenant?.name).toBe('Beta Living Spaces');

    // Verify audit log registration
    expect(state.auditLogs.length).toBeGreaterThan(0);
    expect(state.auditLogs[0].action).toBe('Tenant Switch');
    expect(state.auditLogs[0].tenantId).toBe('tenant-beta');
  });

  // 2. Chat, Citations, and flow data tests
  test('Chat: sending a message updates chat history', () => {
    const store = useStore.getState();
    expect(store.chatHistory.length).toBe(1);

    // Send a message
    store.sendChatMessage('Plumbing repair required in Unit B');
    const state = useStore.getState();
    
    // User message should be appended immediately
    expect(state.chatHistory.length).toBe(2);
    expect(state.chatHistory[1].sender).toBe('user');
    expect(state.chatHistory[1].content).toBe('Plumbing repair required in Unit B');
    expect(state.isLoading).toBe(true);
  });

  test('Chat: simulated AI responses generate citations and flow visualizer data', (done) => {
    const store = useStore.getState();
    store.sendChatMessage('Check my lease rent escalation');

    // Wait for the simulated async agent response (1.5 seconds)
    setTimeout(() => {
      const state = useStore.getState();
      // Should have: 1 welcome msg + 1 user msg + 1 bot response
      expect(state.chatHistory.length).toBe(3);
      
      const botMsg = state.chatHistory[2];
      expect(botMsg.sender).toBe('assistant');
      
      // Grounding sources / Citations validation
      expect(botMsg.citations).toBeDefined();
      expect(botMsg.citations!.length).toBeGreaterThan(0);
      expect(botMsg.citations![0].docName).toBe('Lease_Agreement_Alpha_2026.pdf');
      
      // Flow visualizer (React Flow data structure validation)
      expect(botMsg.flowData).toBeDefined();
      expect(botMsg.flowData?.nodes).toBeDefined();
      expect(botMsg.flowData?.edges).toBeDefined();
      expect(botMsg.flowData!.nodes.length).toBeGreaterThan(0);

      done();
    }, 1600);
  });

  // 3. Action approvals board tests
  test('Approvals: approving a staged request updates status and creates audit log', () => {
    const store = useStore.getState();
    const pendingCount = store.approvals.filter(a => a.status === 'pending').length;
    expect(pendingCount).toBe(1);

    // Approve the request
    store.approveRequest('appr-1');
    const state = useStore.getState();
    const targetApproval = state.approvals.find(a => a.id === 'appr-1');
    expect(targetApproval?.status).toBe('approved');

    // Verify audit logging
    const approveLogs = state.auditLogs.filter(l => l.action === 'Approve Request');
    expect(approveLogs.length).toBe(1);
    expect(approveLogs[0].status).toBe('success');
  });

  test('Approvals: rejecting a staged request updates status and logs as failed task execution', () => {
    const store = useStore.getState();
    store.rejectRequest('appr-1');
    const state = useStore.getState();
    const targetApproval = state.approvals.find(a => a.id === 'appr-1');
    expect(targetApproval?.status).toBe('rejected');

    // Verify audit logging
    const rejectLogs = state.auditLogs.filter(l => l.action === 'Reject Request');
    expect(rejectLogs.length).toBe(1);
    expect(rejectLogs[0].status).toBe('failed');
  });

  // 4. Model Context Protocol tool connector tests
  test('MCP Tools: toggling connector status changes active registry state', () => {
    const store = useStore.getState();
    const initialStatus = store.mcpTools[0].status;
    expect(initialStatus).toBe('active');

    // Toggle tool
    store.toggleMCPTool('tool-lease-analyzer');
    let state = useStore.getState();
    expect(state.mcpTools[0].status).toBe('inactive');

    // Toggle back
    store.toggleMCPTool('tool-lease-analyzer');
    state = useStore.getState();
    expect(state.mcpTools[0].status).toBe('active');
  });

  test('MCP Tools: registering new connector mounts new tool with active status', () => {
    const store = useStore.getState();
    const initialCount = store.mcpTools.length;

    store.addMCPTool({
      name: 'Custom Webhook Checker',
      description: 'Verifies external tenant parameters via hook.',
      endpoint: 'https://api.tenantmind.ai/hooks/check',
      headers: { 'Authorization': 'Bearer sso-key' }
    });

    const state = useStore.getState();
    expect(state.mcpTools.length).toBe(initialCount + 1);
    expect(state.mcpTools[state.mcpTools.length - 1].name).toBe('Custom Webhook Checker');
    expect(state.mcpTools[state.mcpTools.length - 1].status).toBe('active');
  });
});
