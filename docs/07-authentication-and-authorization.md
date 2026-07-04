# 07. Authentication & Authorization

Enterprise authentication is managed by Keycloak (OIDC).

## Flow
1. User requests resource on Frontend.
2. Redirected to Keycloak login page if unauthenticated.
3. Authenticates, receives JWT Access Token, ID Token, and Refresh Token.
4. Frontend attaches Bearer JWT in the `Authorization` header for Backend API calls.
5. FastAPI verifies signature, client audiences, and extracts roles.
