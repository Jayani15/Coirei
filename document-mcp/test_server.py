import asyncio
from server import mcp

async def main():
    tools = await mcp.list_tools()

    print("Registered Tools:\n")

    for tool in tools:
        print(f"- {tool.name}")

asyncio.run(main())