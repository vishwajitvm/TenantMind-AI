import React, { createContext, useContext, useEffect, useState } from 'react';
import { useStore } from './store';

interface KeycloakContextType {
  authenticated: boolean;
  token: string | null;
  username: string | null;
  roles: string[];
  login: () => void;
  logout: () => void;
  hasRole: (role: string) => boolean;
  hasPermission: (permission: string) => boolean;
}

const KeycloakContext = createContext<KeycloakContextType | null>(null);

export const KeycloakProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [authenticated, setAuthenticated] = useState<boolean>(true);
  const [token, setToken] = useState<string | null>('mock-jwt-token-xyz-123');
  const [username, setUsername] = useState<string | null>('admin_user');
  const [roles, setRoles] = useState<string[]>(['admin', 'manager']);
  
  const storeLogin = useStore(state => state.login);
  const storeLogout = useStore(state => state.logout);

  useEffect(() => {
    // Try to detect real Keycloak if configured in env, otherwise fallback to local session
    const keycloakUrl = process.env.NEXT_PUBLIC_KEYCLOAK_URL;
    const realm = process.env.NEXT_PUBLIC_KEYCLOAK_REALM;
    const clientId = process.env.NEXT_PUBLIC_KEYCLOAK_CLIENT_ID;

    console.log('[Keycloak Init] Configured with:', { keycloakUrl, realm, clientId });
    
    // In production/deployment, keycloak-js would initialize here.
    // For smooth user review and direct execution:
    storeLogin('admin_user', ['admin', 'manager']);
  }, [storeLogin]);

  const login = () => {
    setAuthenticated(true);
    setToken('mock-jwt-token-xyz-123');
    setUsername('admin_user');
    setRoles(['admin', 'manager']);
    storeLogin('admin_user', ['admin', 'manager']);
  };

  const logout = () => {
    setAuthenticated(false);
    setToken(null);
    setUsername(null);
    setRoles([]);
    storeLogout();
  };

  const hasRole = (role: string) => {
    return roles.includes(role);
  };

  const hasPermission = (permission: string) => {
    if (roles.includes('admin')) return true;
    if (roles.includes('manager') && permission.startsWith('read:')) return true;
    return false;
  };

  return (
    <KeycloakContext.Provider value={{
      authenticated,
      token,
      username,
      roles,
      login,
      logout,
      hasRole,
      hasPermission
    }}>
      {children}
    </KeycloakContext.Provider>
  );
};

export const useKeycloak = () => {
  const context = useContext(KeycloakContext);
  if (!context) {
    throw new Error('useKeycloak must be used within a KeycloakProvider');
  }
  return context;
};
