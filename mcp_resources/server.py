from mcp.server.fastmcp import FastMCP


mcp = FastMCP(name='Resources', stateless_http=True)

docs= {
  'intro': 'This is the introduction to mcp server',
  'guide': 'This is a guide to use the mcp server',
  'readme': 'This is the readme of mcp server'
  }


@mcp.resource('docs://documents',mime_type='application/json')
async def list_docs():
  return list(docs.keys())

@mcp.resource("file://data/main.py",mime_type='application/json')
def read_file():
  with open('data/main.py','r') as f:
    content = f.read()
    return content
  
  


@mcp.resource('docs://documents/{doc_id}',mime_type='application/json')
def read_docs(doc_id:str):
  if doc_id in docs:
    return {'name': doc_id, 'content': docs[doc_id]}
  else:
    raise {f"document  {doc_id} not found"} 

mcp_app = mcp.streamable_http_app()