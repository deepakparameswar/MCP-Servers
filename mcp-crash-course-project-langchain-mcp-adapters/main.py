import asyncio
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from mcp import ClientSession, StdioServerParameters
# ClientSession will provide an framwork to act as a MCP Client
# StdioServerParameters will provide the parameters to start a MCP server
from mcp.client.stdio import stdio_client
# stdio_client is going to communicate to the MCP server via transport layer of stdio, means it going to read from standatd input and write to standard output
# thats how client is going to communicate with the MCP server

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="qwen/qwen3-32b", temperature=0)

stdio_server_params = StdioServerParameters(
    command="python",
    args=["D:/Projects/MCPs/mcp-servers/mcp-crash-course-project-langchain-mcp-adapters/servers/math_server.py"],
)

async def main():
    async with stdio_client(stdio_server_params) as (read,write):    
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("session initialized")
            tools = await load_mcp_tools(session)

            print(f"tools: {tools}")

            agent = create_agent(llm,tools)

            result = await agent.ainvoke({"messages": [HumanMessage(content="What is 54 + 2 * 3?")]})
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())

