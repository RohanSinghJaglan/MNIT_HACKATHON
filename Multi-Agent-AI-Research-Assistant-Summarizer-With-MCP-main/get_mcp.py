from mcp_use import MCPAgent,MCPClient
from dotenv import load_dotenv
import os
from llm import get_llm


load_dotenv()

gemin_llm=get_llm()


config={
  "mcpServers": {
    "duckduckgo-search": {
        "command": "npx",
        "args": [
          "-y",
          "duckduckgo-mcp-server"
        ]
    },
    "bright_data": {
        "command": "npx",
        "args": ["@brightdata/mcp"],
        "env": {
            "API_TOKEN": os.getenv("BRIGHT_DATA_API_TOKEN"),
            "WEB_UNLOCKER_ZONE": os.getenv("WEB_UNLOCKER_ZONE", "unblocker"),
            "BROWSER_ZONE": os.getenv("BROWSER_ZONE", "scraping_browser")
        }
    }
  }
}

client=MCPClient.from_dict(config)

agent=MCPAgent(
    llm=gemin_llm,
    client=client,
    max_steps=15,
    memory_enabled=True
)

async def get_mcp_use(prompt_text: str):
    return await agent.run(prompt_text)

