import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer

from server.tools.tools import register_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables from the repo root, regardless of the process cwd
load_dotenv(Path(__file__).resolve().parent / ".env")


# Initialize MCP server
mcp = MCPServer("Trello MCP Server")

# Register tools
register_tools(mcp)


def start_claude_server():
    """Start the MCP server in Claude app mode"""
    try:
        # Verify environment variables
        if not os.getenv("TRELLO_API_KEY") or not os.getenv("TRELLO_TOKEN"):
            raise ValueError(
                "TRELLO_API_KEY and TRELLO_TOKEN must be set in environment variables"
            )

        logger.info("Starting Trello MCP Server in Claude app mode...")
        mcp.run()
        logger.info("Trello MCP Server started successfully")
    except Exception as e:
        logger.error(f"Error starting Claude server: {str(e)}")
        raise


def start_sse_server():
    """Start the MCP server in SSE mode using uvicorn"""
    try:
        # Verify environment variables
        if not os.getenv("TRELLO_API_KEY") or not os.getenv("TRELLO_TOKEN"):
            raise ValueError(
                "TRELLO_API_KEY and TRELLO_TOKEN must be set in environment variables"
            )

        host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
        port = int(os.getenv("MCP_SERVER_PORT", "8000"))

        logger.info(
            f"Starting Trello MCP Server in SSE mode on http://{host}:{port}..."
        )
        mcp.run(transport="sse", host=host, port=port)
    except Exception as e:
        logger.error(f"Error starting SSE server: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        # Check which mode to run in (default to true for Claude app mode)
        use_claude = os.getenv("USE_CLAUDE_APP", "true").lower() == "true"

        if use_claude:
            # Run in Claude app mode
            start_claude_server()
        else:
            # Run in SSE mode
            start_sse_server()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise
