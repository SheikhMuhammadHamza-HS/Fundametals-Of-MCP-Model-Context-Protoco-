from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP(name='hello_mcp',stateless_http=True)


def load_data():
    with open('data.json','r')as f:
        data = json.load(f)
        return data

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data,f)
        
    
@mcp.tool(
    name='read_document',
    description='Read the content of documents and returns it as a string'
)
async def read_document(doc_id:str):
    # load data
    data = load_data()
    
    if doc_id not in data:
        return ValueError(f"doc with id {doc_id} not found")
    return data[doc_id]

@mcp.tool(
    name="edit_document",
    description='edit the document by replacing a string in the documents content with a new string'
)

def edit_document(doc_id:str,old_val:str,new_val:str):
    # load data
    data = load_data()
    
    if doc_id not in data:
        raise ValueError(f"doc with id {doc_id} not found")
    #  spec.txt  
    data[doc_id] = data[doc_id].replace(old_val,new_val)
    save_data(data)
    return data[doc_id]
    
    
    

mcp_app = mcp.streamable_http_app()