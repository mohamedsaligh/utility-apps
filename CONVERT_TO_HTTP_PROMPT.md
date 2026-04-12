# Prompt: Convert Confluence MCP Server from stdio/SSE to Streamable HTTP

## Context

This is a Confluence MCP server project built with FastMCP (Python). It currently runs with SSE transport and has a `main()` entry point that uses `mcp.run()` (stdio). I need to convert it so GitHub Copilot (VS Code) can connect to it remotely via `"type": "http"` (Streamable HTTP transport) from any machine.

The server runs on a **remote machine**. The `CONFLUENCE_API_KEY` (base64-encoded `username:api_token`) must be passed **from the IDE** via an HTTP header, NOT hardcoded on the server.

## Current Project Structure

```
source/
├── __main__.py          # FastMCP server entry point (SSE + stdio)
├── __init__.py
├── confluence_client.py # Confluence client with token refresh scheduler
├── confluence_tools.py  # MCP tool registrations
├── resources/
│   └── __init__.py      # app_config
├── authentication/
│   ├── Authentication.py      # Abstract base class
│   ├── EnvAuthentication.py   # Reads token from env var
│   └── TokenManager.py        # Token manager
```

## Required Changes — Do ALL of these:

### 1. Modify `__main__.py`

Replace the current SSE + stdio setup with **streamable-http** transport:

```python
# REMOVE these lines:
#   mcp_app = mcp.http_app(transport="sse")
#   app = FastAPI()
#   app.mount("/", mcp_app)
#   def main():
#       mcp.run()

# REPLACE with streamable-http setup:
```

- Use `mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)` as the entry point.
- OR if you need the FastAPI wrapper for the health endpoint, do:

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS - allow all origins for MCP client connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint
@app.get("/actuator/health")
async def health_check():
    return {"status": "healthy"}

# Mount MCP with streamable-http transport
mcp_app = mcp.http_app(transport="streamable-http", path="/mcp")
app.mount("/", mcp_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### 2. Add Authentication Middleware to Accept API Key from HTTP Headers

Create a new middleware that intercepts the `Authorization` or `X-Confluence-Token` header from the incoming MCP request and sets it as an environment variable so the existing `EnvAuthentication` + `TokenManager` flow continues to work.

Create `source/auth_middleware.py`:

```python
import os
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)

class MCPAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that extracts the Confluence API token from the
    incoming HTTP request header and sets it as an environment
    variable so the existing EnvAuthentication class can read it.
    
    Accepts token from either:
      - Authorization: Bearer <token>
      - X-Confluence-Token: <token>
    """
    async def dispatch(self, request: Request, call_next):
        token = None
        
        # Try Authorization header first
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
        
        # Fallback to custom header
        if not token:
            token = request.headers.get("X-Confluence-Token", "")
        
        if token:
            os.environ["CONFLUENCE_API_TOKEN"] = token
            logger.debug("Set CONFLUENCE_API_TOKEN from request header")
        
        response = await call_next(request)
        return response
```

Then in `__main__.py`, add this middleware to the FastAPI app:

```python
from .auth_middleware import MCPAuthMiddleware
app.add_middleware(MCPAuthMiddleware)
```

**IMPORTANT:** Add the auth middleware BEFORE the CORS middleware (middleware executes in reverse order of addition, so add CORS first, then auth).

### 3. Update `EnvAuthentication.py`

Ensure the `token_env_var` config default matches the header middleware. The current code reads from `config.get('token_env_var', f'{service_name.upper()}_API_TOKEN')`, so if the service name is "confluence", it will look for `CONFLUENCE_API_TOKEN`. This should match what the middleware sets. Verify this matches and fix if needed.

### 4. Update `confluence_client.py`

No major changes needed, but ensure `update_confluence_client()` is resilient to token changes mid-session (since the token now comes per-request from headers). The lazy initialization pattern already handles this.

### 5. Update `requirements.txt`

Ensure these are present:

```
fastmcp>=2.0.0
uvicorn
fastapi
starlette
atlassian-python-api
schedule
```

### 6. Update the run command

The server should be started with:

```bash
# Option A: Direct python
python -m source

# Option B: Uvicorn (recommended for production)
uvicorn source.__main__:app --host 0.0.0.0 --port 8080
```

### 7. IDE Configuration (for reference)

On the VS Code side, the `mcp.json` should be configured as:

```json
{
  "servers": {
    "confluence": {
      "type": "http",
      "url": "http://<REMOTE_SERVER_IP>:8080/mcp",
      "headers": {
        "Authorization": "Bearer ${input:confluenceToken}"
      }
    }
  },
  "inputs": [
    {
      "id": "confluenceToken",
      "type": "promptString",
      "description": "Confluence API Token (base64 encoded username:token)",
      "password": true
    }
  ]
}
```

Or if the token should be hardcoded per-workspace (not prompted every time):

```json
{
  "servers": {
    "confluence": {
      "type": "http",
      "url": "http://<REMOTE_SERVER_IP>:8080/mcp",
      "headers": {
        "Authorization": "Bearer <BASE64_ENCODED_USERNAME:API_TOKEN>"
      }
    }
  }
}
```

## Constraints

- Do NOT break the existing `confluence_tools.py` — the MCP tool registrations must remain unchanged.
- Do NOT change the `resources/` config loading.
- Keep the health endpoint at `/actuator/health`.
- The MCP endpoint MUST be at `/mcp` (this is what VS Code will connect to).
- Keep all existing logging.
- The server must work when accessed from a different machine over the network.
- Use `transport="streamable-http"` NOT `transport="sse"` (SSE is deprecated in MCP spec).
- Ensure the FastMCP version supports streamable-http (fastmcp >= 2.0.0).
- Keep the background scheduler thread for token refresh intact.
- Test that the `/mcp` endpoint responds to MCP protocol initialization.

## Verification Steps After Conversion

1. Start the server: `uvicorn source.__main__:app --host 0.0.0.0 --port 8080`
2. Verify health: `curl http://localhost:8080/actuator/health` → should return `{"status": "healthy"}`
3. Verify MCP endpoint exists: `curl -X POST http://localhost:8080/mcp -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'` → should return MCP initialize response
4. In VS Code, configure `mcp.json` with `"type": "http"` pointing to the server, verify tools appear in Copilot agent mode.

Now apply all changes to make this work.
