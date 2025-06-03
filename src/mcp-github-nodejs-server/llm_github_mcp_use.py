import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient
"""
pip install mcp-use
"""
async def main():
    # Load environment variables
    load_dotenv()

    # Create configuration dictionary
    config = {
        "mcpServers": {
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "<GITHUB PERSONAL ACCESS TOKEN>"
            }
        }
        }
    }

    # Create MCPClient from configuration dictionary
    client = MCPClient.from_dict(config)

    # Create LLM
    llm = ChatOpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),
                     base_url="https://api.deepseek.com",
                     model="deepseek-chat")

    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    # Run the query
    result = await agent.run(
        "搜索 ai-agent-demo repo, 作者为Liu-Shihao",
    )
    print(f"\nResult: {result}")

if __name__ == "__main__":
    asyncio.run(main())
    """
    GitHub MCP Server running on stdio

    Result: 找到了名为 `ai-agent-demo` 的仓库，作者是 `Liu-Shihao`。以下是该仓库的详细信息：
    
    - **仓库名称**: ai-agent-demo
    - **作者**: Liu-Shihao
    - **描述**: 使用LangGraph构建Multi-Agent应用程序
    - **仓库链接**: [https://github.com/Liu-Shihao/ai-agent-demo](https://github.com/Liu-Shihao/ai-agent-demo)
    - **创建时间**: 2025-03-17
    - **最后更新时间**: 2025-06-03
    - **默认分支**: main
    
    如果需要进一步操作或查看该仓库的内容，请告诉我！
    """