

import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client


class MCPClient:
    def __init__(
        self,
        server_url: str,
    ):
        self._server_url = server_url
        self._session: Optional[ClientSession] = None
        self._exit_stack: AsyncExitStack = AsyncExitStack()

    async def connect(self):
        streamable_transport = await self._exit_stack.enter_async_context(
            streamablehttp_client(self._server_url)
        )
        _read, _write, _get_session_id = streamable_transport
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(_read, _write)
        )
        await self._session.initialize()

    def session(self) -> ClientSession:
        if self._session is None:
            raise ConnectionError(
                "Client session not initialized or cache not populated. Call connect_to_server first."
            )
        return self._session

    async def list_prompts(self):
        result = await self._session.list_prompts()
        return result.prompts
    
    async def get_prompt(self,prompt_name:str,arg:dict[str,str]):
        result = await self._session.get_prompt(prompt_name,arg)
        return result

    async def cleanup(self):
        await self._exit_stack.aclose()
        self._session = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()




async def main():
    async with MCPClient(
        server_url="http://localhost:8000/mcp/",
    ) as _client:
        # Example usage:
        # Retrieve and print available tools to verify the client implementation.
        # prompts = await _client.list_prompts()
        # print("Available Tools:", prompts)
        prompt = await _client.get_prompt('user_error_prompt',{'error': 'function error'})
        for item in prompt.messages:
            print(f"role: {item.role},{item.content.text}")


asyncio.run(main())
