#!/bin/bash
# ------------------------------------------------------------------------------
# TenantMind AI - API Verification Script
# ------------------------------------------------------------------------------

BASE_URL="http://localhost:8000"
TENANT="default"

echo "=== Starting API Verification Tests ==="
echo "Target Host: $BASE_URL"
echo "Tenant Header: X-Tenant-ID = $TENANT"
echo "---------------------------------------"

# Helper for GET requests
test_get() {
  local endpoint=$1
  echo -n "GET $endpoint... "
  local response=$(curl -s -o /dev/null -w "%{http_code}" -H "X-Tenant-ID: $TENANT" "$BASE_URL$endpoint")
  if [ "$response" -eq 200 ] || [ "$response" -eq 201 ]; then
    echo "PASS ($response)"
  else
    echo "FAIL ($response)"
  fi
}

# Helper for POST requests
test_post() {
  local endpoint=$1
  local data=$2
  echo -n "POST $endpoint... "
  local response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -H "X-Tenant-ID: $TENANT" -d "$data" "$BASE_URL$endpoint")
  if [ "$response" -eq 200 ] || [ "$response" -eq 201 ]; then
    echo "PASS ($response)"
  else
    echo "FAIL ($response)"
  fi
}

# 1. Health and Readiness
test_get "/health"
test_get "/ready"

# 2. Organizations
test_post "/api/organizations" '{"name": "Default Test Org", "slug": "default"}'
test_get "/api/organizations"

# 3. Documents
test_get "/api/documents"

# 4. Chats
test_post "/api/chat" '{"messages": [{"role": "user", "content": "Hello AI assistant!"}], "use_rag": false}'
test_get "/api/chat/sessions"

# 5. RAG query
test_post "/api/rag/query" '{"query": "Is there a config file?", "limit": 2}'

# 6. Models and Tools
test_get "/api/models/health"
test_get "/api/mcp/tools"

# 7. Approvals & Audit logs
test_get "/api/approvals"
test_get "/api/audit-logs"

echo "---------------------------------------"
echo "=== API Verification Complete ==="
