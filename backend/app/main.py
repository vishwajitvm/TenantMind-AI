from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from app.middleware import TenantMiddleware, TraceNestMiddleware
from app.api import chats, documents, approvals, audit_logs, models, health, organizations, rag, mcp, users
from app.config import settings
from tracenest import logger

# Initialize FastAPI App
app = FastAPI(
    title="TenantMind AI API",
    description="Multitenant AI Backend API with strict isolation, LLM fallback gateways, and MCP tool validation.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Middleware
app.add_middleware(TraceNestMiddleware)
app.add_middleware(TenantMiddleware)

# Custom Exception Handlers for logging
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global unhandled exception on {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."}
    )

# Register Routers (register both with and without '/api' prefix for routing flexibility)
for router_module in [chats, documents, approvals, audit_logs, models, health, organizations, rag, mcp, users]:
    app.include_router(router_module.router, prefix="/api")
    app.include_router(router_module.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to TenantMind AI API Gateway",
        "version": "1.0.0",
        "status": "online"
    }

import os
import glob
import json

def read_tracenest_logs_data(limit: int = 150):
    app_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(app_dir)
    logs_dir = os.path.join(backend_dir, "TraceNestLogs")
    
    if not os.path.exists(logs_dir):
        return {"logs": [], "metrics": {"total_requests": 0, "errors": 0, "avg_latency": 0.0, "status_codes": {}}}
        
    log_files = glob.glob(os.path.join(logs_dir, "*.log"))
    if not log_files:
        return {"logs": [], "metrics": {"total_requests": 0, "errors": 0, "avg_latency": 0.0, "status_codes": {}}}
        
    log_files.sort()
    latest_file = log_files[-1]
    
    logs = []
    total_requests = 0
    errors = 0
    latencies = []
    status_codes = {}
    
    try:
        with open(latest_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in reversed(lines):
                line = line.strip()
                if not line:
                    continue
                try:
                    log_data = json.loads(line)
                    logs.append(log_data)
                    
                    level = log_data.get("level", "INFO")
                    message = log_data.get("message", "")
                    
                    if level == "ERROR":
                        errors += 1
                        
                    if "Request Completed:" in message:
                        total_requests += 1
                        status_part = [p for p in message.split("|") if "Status:" in p]
                        duration_part = [p for p in message.split("|") if "Duration:" in p]
                        
                        if status_part:
                            status_code = status_part[0].replace("Status:", "").strip()
                            status_codes[status_code] = status_codes.get(status_code, 0) + 1
                        if duration_part:
                            try:
                                duration_val = float(duration_part[0].replace("Duration:", "").replace("s", "").strip())
                                latencies.append(duration_val)
                            except ValueError:
                                pass
                except Exception:
                    pass
    except Exception as e:
        pass
        
    display_logs = logs[:limit]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    
    return {
        "logs": display_logs,
        "metrics": {
            "total_requests": total_requests,
            "errors": errors,
            "avg_latency": round(avg_latency, 4),
            "status_codes": status_codes,
            "log_file": os.path.basename(latest_file)
        }
    }

@app.get("/tracenest/logs")
async def tracenest_logs_api(limit: int = 150):
    """Exposes structured logs and calculated system metrics for the dashboard."""
    return read_tracenest_logs_data(limit=limit)

@app.get("/tracenest", response_class=HTMLResponse)
async def tracenest_ui():
    """Renders a beautiful, real-time structured logging and system health dashboard."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TraceNest Telemetry Engine</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-darker: #05050c;
            --bg-dark: #090915;
            --bg-card: #0e0e24;
            --border: #1d1d42;
            --text-main: #f1f1f7;
            --text-muted: #8484a3;
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --info: #06b6d4;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-darker);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* Scrollbars */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-darker);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary);
        }

        header {
            background-color: var(--bg-dark);
            border-bottom: 1px solid var(--border);
            padding: 1.25rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(12px);
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .pulse-indicator {
            width: 10px;
            height: 10px;
            background-color: var(--success);
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 10px var(--success);
            animation: pulse 1.8s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        .logo-section h1 {
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            background: linear-gradient(135deg, #fff 0%, var(--primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .logo-section span {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            background-color: var(--border);
            color: var(--primary);
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-weight: bold;
        }

        .controls {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .auto-refresh {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.85rem;
            color: var(--text-muted);
            cursor: pointer;
            user-select: none;
        }

        .auto-refresh input {
            accent-color: var(--primary);
            width: 16px;
            height: 16px;
            cursor: pointer;
        }

        .refresh-btn {
            background-color: var(--primary);
            color: #fff;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
        }

        .refresh-btn:hover {
            background-color: var(--primary-hover);
            transform: translateY(-1px);
        }

        main {
            padding: 2rem;
            flex: 1;
            max-width: 1600px;
            width: 100%;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-cols: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.25rem;
        }

        .stat-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 110px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            position: relative;
            overflow: hidden;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: var(--primary);
        }

        .stat-card.errors::before { background: var(--error); }
        .stat-card.success::before { background: var(--success); }
        .stat-card.info::before { background: var(--info); }

        .stat-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 800;
            margin-top: 0.5rem;
            font-family: 'Outfit', sans-serif;
        }

        .stat-desc {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
            font-family: 'JetBrains Mono', monospace;
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
        }

        /* Main Workspace Container */
        .workspace {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }

        .panel {
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 4px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }

        .panel-header {
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: var(--bg-dark);
        }

        .panel-title {
            font-size: 1.1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .search-filters {
            display: flex;
            gap: 0.75rem;
            align-items: center;
            flex-wrap: wrap;
        }

        .search-box {
            background-color: var(--bg-darker);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            min-width: 240px;
            outline: none;
            transition: all 0.2s ease;
        }

        .search-box:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15);
        }

        .filter-btn-group {
            display: flex;
            background-color: var(--bg-darker);
            border: 1px solid var(--border);
            padding: 0.2rem;
            border-radius: 8px;
        }

        .filter-btn {
            background: none;
            border: none;
            color: var(--text-muted);
            padding: 0.35rem 0.75rem;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .filter-btn:hover {
            color: var(--text-main);
        }

        .filter-btn.active {
            background-color: var(--primary);
            color: #fff;
        }

        /* Logs Table/List */
        .logs-container {
            max-height: 600px;
            overflow-y: auto;
        }

        .logs-list {
            display: flex;
            flex-direction: column;
            width: 100%;
        }

        .log-row {
            display: flex;
            flex-direction: column;
            padding: 0.85rem 1.5rem;
            border-bottom: 1px solid rgba(29, 29, 66, 0.4);
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .log-row:hover {
            background-color: rgba(99, 102, 241, 0.03);
        }

        .log-row.expanded {
            background-color: rgba(99, 102, 241, 0.05);
            border-left: 3px solid var(--primary);
        }

        .log-header-info {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            font-size: 0.85rem;
        }

        .log-left {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            min-width: 0;
            flex: 1;
        }

        .log-badge {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            font-weight: 700;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.025em;
            flex-shrink: 0;
        }

        .log-badge.info { background-color: rgba(6, 182, 212, 0.1); color: var(--info); border: 1px solid rgba(6, 182, 212, 0.2); }
        .log-badge.warning { background-color: rgba(245, 158, 11, 0.1); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.2); }
        .log-badge.error { background-color: rgba(239, 68, 68, 0.1); color: var(--error); border: 1px solid rgba(239, 68, 68, 0.2); }

        .log-timestamp {
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            white-space: nowrap;
        }

        .log-msg {
            font-weight: 500;
            color: var(--text-main);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 0.85rem;
        }

        .log-row.expanded .log-msg {
            white-space: normal;
            word-break: break-all;
        }

        .log-meta-tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: var(--text-muted);
            background-color: var(--bg-darker);
            padding: 0.15rem 0.35rem;
            border-radius: 4px;
            border: 1px solid var(--border);
            white-space: nowrap;
        }

        .log-details-block {
            display: none;
            margin-top: 0.75rem;
            padding: 1rem;
            background-color: var(--bg-darker);
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow-x: auto;
        }

        .log-row.expanded .log-details-block {
            display: block;
        }

        .log-details-block pre {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            line-height: 1.4;
            color: #d1d1f7;
        }

        .no-logs {
            padding: 4rem 2rem;
            text-align: center;
            color: var(--text-muted);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1rem;
        }

        .no-logs svg {
            width: 48px;
            height: 48px;
            stroke: var(--border);
        }

        footer {
            margin-top: auto;
            padding: 1.5rem 2rem;
            border-top: 1px solid var(--border);
            text-align: center;
            font-size: 0.75rem;
            color: var(--text-muted);
            background-color: var(--bg-dark);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        footer a {
            color: var(--primary);
            text-decoration: none;
        }

        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <div class="logo-section">
            <div class="pulse-indicator"></div>
            <h1>TraceNest Telemetry Console</h1>
            <span>v0.1.7</span>
        </div>
        <div class="controls">
            <label class="auto-refresh">
                <input type="checkbox" id="autoRefreshCheckbox" checked>
                Auto-Refresh (3s)
            </label>
            <button class="refresh-btn" id="refreshBtn">Fetch Logs</button>
        </div>
    </header>

    <main>
        <!-- Stats Dashboard -->
        <div class="stats-grid">
            <div class="stat-card info">
                <div class="stat-label">Telemetry Engine</div>
                <div class="stat-value" id="totalRequests">0</div>
                <div class="stat-desc">Total tracked HTTP calls</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Average Performance</div>
                <div class="stat-value" id="avgLatency">0.00s</div>
                <div class="stat-desc">Process latency duration</div>
            </div>
            <div class="stat-card errors">
                <div class="stat-label">System Failures</div>
                <div class="stat-value" id="totalErrors">0</div>
                <div class="stat-desc">Tracked Exception errors</div>
            </div>
            <div class="stat-card success">
                <div class="stat-label">Active Log Stream</div>
                <div class="stat-value" style="font-size: 1rem; font-family: 'Outfit', sans-serif; word-break: break-all;" id="logFileName">-</div>
                <div class="stat-desc">Current Log file target</div>
            </div>
        </div>

        <!-- Logs Panel -->
        <div class="workspace">
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">
                        Log Operations Feed
                    </div>
                    <div class="search-filters">
                        <input type="text" class="search-box" id="searchBox" placeholder="Filter message details...">
                        
                        <div class="filter-btn-group">
                            <button class="filter-btn active" data-level="ALL">ALL</button>
                            <button class="filter-btn" data-level="INFO">INFO</button>
                            <button class="filter-btn" data-level="WARNING">WARN</button>
                            <button class="filter-btn" data-level="ERROR">ERROR</button>
                        </div>
                    </div>
                </div>

                <div class="logs-container">
                    <div class="logs-list" id="logsList">
                        <!-- Loaded dynamically -->
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer>
        <div>TenantMind AI Production Logging Engine</div>
        <div>Connected to <a href="/docs" target="_blank">FastAPI OpenAPI docs</a></div>
    </footer>

    <script>
        let currentFilter = 'ALL';
        let searchQuery = '';
        let logsData = [];
        let autoRefreshInterval = null;

        document.addEventListener('DOMContentLoaded', () => {
            fetchLogs();
            setupAutoRefresh();

            document.getElementById('refreshBtn').addEventListener('click', fetchLogs);
            
            document.getElementById('searchBox').addEventListener('input', (e) => {
                searchQuery = e.target.value.toLowerCase();
                renderLogs();
            });

            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                    e.target.classList.add('active');
                    currentFilter = e.target.getAttribute('data-level');
                    renderLogs();
                });
            });

            document.getElementById('autoRefreshCheckbox').addEventListener('change', setupAutoRefresh);
        });

        function setupAutoRefresh() {
            const isChecked = document.getElementById('autoRefreshCheckbox').checked;
            if (isChecked) {
                if (!autoRefreshInterval) {
                    autoRefreshInterval = setInterval(fetchLogs, 3000);
                }
            } else {
                if (autoRefreshInterval) {
                    clearInterval(autoRefreshInterval);
                    autoRefreshInterval = null;
                }
            }
        }

        async function fetchLogs() {
            try {
                const response = await fetch('/tracenest/logs');
                if (!response.ok) throw new Error('API server returned status: ' + response.status);
                
                const data = await response.json();
                logsData = data.logs || [];
                
                // Update metrics dashboard
                const metrics = data.metrics || {};
                document.getElementById('totalRequests').innerText = metrics.total_requests || 0;
                document.getElementById('avgLatency').innerText = (metrics.avg_latency || 0.0) + 's';
                document.getElementById('totalErrors').innerText = metrics.errors || 0;
                document.getElementById('logFileName').innerText = metrics.log_file || '-';
                
                renderLogs();
            } catch (err) {
                console.error('Failed to load telemetry logs:', err);
            }
        }

        function renderLogs() {
            const container = document.getElementById('logsList');
            container.innerHTML = '';
            
            const filtered = logsData.filter(log => {
                const matchesLevel = currentFilter === 'ALL' || log.level === currentFilter;
                const message = (log.message || '').toLowerCase();
                const matchesSearch = !searchQuery || message.includes(searchQuery);
                return matchesLevel && matchesSearch;
            });

            if (filtered.length === 0) {
                container.innerHTML = `
                    <div class="no-logs">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width:48px;height:48px;stroke:var(--border);">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
                        </svg>
                        <p>No telemetry logs match the current search or filters.</p>
                    </div>
                `;
                return;
            }

            filtered.forEach((log, index) => {
                const levelClass = log.level ? log.level.toLowerCase() : 'info';
                const timestamp = log.ts || log.timestamp || '';
                const displayTime = timestamp.split('T')[1] ? timestamp.split('T')[1].substring(0, 8) : timestamp;
                const message = log.message || '';
                const project = log.project || 'TraceNest';
                
                const row = document.createElement('div');
                row.className = 'log-row';
                row.innerHTML = `
                    <div class="log-header-info">
                        <div class="log-left">
                            <span class="log-badge ${levelClass}">${log.level}</span>
                            <span class="log-timestamp">${displayTime}</span>
                            <span class="log-msg">${message}</span>
                        </div>
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            <span class="log-meta-tag">${project}</span>
                        </div>
                    </div>
                    <div class="log-details-block">
                        <pre><code>${JSON.stringify(log, null, 4)}</code></pre>
                    </div>
                `;
                
                row.addEventListener('click', (e) => {
                    if (e.target.tagName === 'CODE' || e.target.tagName === 'PRE') return;
                    row.classList.toggle('expanded');
                });

                container.appendChild(row);
            });
        }
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content, status_code=200)
