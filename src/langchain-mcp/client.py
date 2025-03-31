# Create server parameters for stdio connection
import os

from langchain_deepseek import ChatDeepSeek
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent



os.environ["DEEPSEEK_API_KEY"] = "..."

model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

"""
pip install langchain-mcp-adapters
"""
# server_params = StdioServerParameters(
#     command="python",
#     # Make sure to update to the full absolute path to your math_server.py file
#     args=["./math_server.py"],
# )
#
# async with stdio_client(server_params) as (read, write):
#     async with ClientSession(read, write) as session:
#         # Initialize the connection
#         await session.initialize()
#
#         # Get tools
#         tools = await load_mcp_tools(session)
#
#         # Create and run the agent
#         agent = create_react_agent(model, tools)
#         agent_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})


async with MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["/Users/liushihao/PycharmProjects/ai-agent-demo/src/langchain-mcp/math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            # make sure you start your weather server on port 8000
            "url": "http://localhost:8000/sse",
            "transport": "sse",
        }
    }
) as client:
    agent = create_react_agent(model, client.get_tools())
    math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
    weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})