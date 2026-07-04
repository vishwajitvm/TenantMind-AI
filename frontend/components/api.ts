import { useStore } from './store';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchWithTenant(endpoint: string, options: RequestInit = {}) {
  const state = useStore.getState();
  const tenantId = state.selectedTenant?.id;
  
  const headers = new Headers(options.headers || {});
  
  // Dynamic Tenant Header injection
  if (tenantId) {
    headers.set('X-Tenant-ID', tenantId);
  }
  
  // Keycloak authorization token placeholder/integration
  headers.set('Authorization', 'Bearer mock-jwt-token-xyz-123');
  headers.set('Content-Type', 'application/json');

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}
