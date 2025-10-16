import asyncio
from mcp import ClientSession,types
from mcp.client.streamable_http import streamablehttp_client
from contextlib import AsyncExitStack
from typing import Optional
from pydantic import AnyUrl
import json

class MCPClient:
  def __init__(
      self,
      server_url:str,
    ):
      self._server_url = server_url
      self._session:Optional[ClientSession] = None
      self._exit_stack: AsyncExitStack = AsyncExitStack()
    
    
  async def connection(self):
    streamable_transport = await self._exit_stack.enter_async_context(
      streamablehttp_client(self._server_url)
    ) # connection banana
    
    
    # connection banjye tu session ko manage krna
    _read,_write  , _get_session_id = streamable_transport
    self._session = await self._exit_stack.enter_async_context(
      ClientSession(_read,_write)
    )
    # session ko initialize krna
    await self._session.initialize()
  
  # after working close the session
  async def cleanUp(self):
    await self._exit_stack.aclose()
    self.session = None
    
  async def __aenter__(self):
    await self.connection()
    return self
  
  async def __aexit__(self,exc_type,exc,tb):
    await self.cleanUp()
  
  
  def session(self)-> ClientSession:
    if self._session is None:
      raise ConnectionError(
       'Client session is not initialized or cache not populated. call connect to sever first' 
      )
  
  async def list_tools(self):
    result = await self._session.list_tools()
    return result.tools  
  
  async def list_resources(self):
    result = await self._session.list_resources()
    return result.resources
  
  async def read_resource(self, uri:AnyUrl) -> types.ReadResourceResult:
    result = await self._session.read_resource(AnyUrl(uri))
    resource = result.contents[0]
    if isinstance(resource,types.TextResourceContents):
      if resource.mimeType == 'application/json':
        try:
            return json.loads(resource.text)
        except json.JSONDecodeError as e: #when json is not correct format
          print(f'Error decoding json {e}')
      return resource.text
        
  async def list_resource_template(self) -> types.ListResourceTemplatesResult:
    result = await self._session.list_resource_templates()
    return result.resourceTemplates
    # print(f"resource template: {result.resourceTemplates}") 
    
    
  
  
async def main():
  async with MCPClient(server_url="http://localhost:8000/mcp/") as _client:
    tools = await _client.list_tools()
    print(f'Available Tools: {tools}')
    
  async with MCPClient(server_url="http://localhost:8000/mcp/") as _client:
    resources = await _client.list_resources()
    
    # static way
    # print(f"Resources: {resources}")
    read_resource = await _client.read_resource('docs://documents')
    print(f"Read Resource: {read_resource}")
    
    # dynamic way
    read_resource_template = await _client.list_resource_template()
    # print(f"Resource template: {read_resource_template[0].uriTemplate}")
    intro_uri = read_resource_template[0].uriTemplate.replace('{doc_id}', 'intro')
    data = await _client.read_resource(intro_uri)
    print(f"Intro Document: {data}")
    
    
asyncio.run(main())      