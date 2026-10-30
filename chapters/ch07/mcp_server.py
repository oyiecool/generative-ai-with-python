# chapters/ch07/mcp_server.py   (uv add "mcp[cli]")
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server-diagnostics")


@mcp.tool()
def service_status(name: str) -> str:
    """Check whether a systemd service is active."""
    return service_status_impl(name)   # reuse your validated implementation


if __name__ == "__main__":
    mcp.run()
