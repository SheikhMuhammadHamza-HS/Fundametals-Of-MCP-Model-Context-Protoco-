from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="mcp_client",stateless_http=True)


docs= {
  'intro': 'This is the introduction to mcp server',
  'guide': 'This is a guide to use the mcp server',
  'readme': 'This is the readme of mcp server'
  }

@mcp.tool(
  name='get_weather',
  description="fetch the weather based on user input"
)
async def get_weather(city:str)->str:
  return f'the weather of {city} is cloudy'

@mcp.resource('docs://documents',mime_type='application/json')
async def list_docs():
  return list(docs.keys())

@mcp.resource('docs://documents/{doc_id}',mime_type='application/json')
def read_docs(doc_id:str):
  if doc_id in docs:
    return {'name': doc_id, 'content': docs[doc_id]}
  else:
    raise {f"document  {doc_id} not found"} 


mcp_app = mcp.streamable_http_app()