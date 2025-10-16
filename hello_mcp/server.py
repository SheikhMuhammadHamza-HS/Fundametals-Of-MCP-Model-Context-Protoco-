from mcp.server.fastmcp import FastMCP #import class FastMCP
from pydantic import Field
mcp = FastMCP(name="hello-mcp",stateless_http=True) #define a instance
 
# run on http and stateless mode

@mcp.tool(name="online_search", description= "Search online for a query")
def search_online(query:str):
    # implement search logic here
    return f"Searching online for: {query}"

docs = {
    "deposition": "This deposition covers the testimony of Angela Smith, P.E.",
    "report": "The report details the state of a 20m condenser tower.",
    "financials": "These financials outline the project's budget and expenditures.",
    "outlook": "This document presents the projected future performance of the system.",
    "plan": "The plan outlines the steps for the project's implementation.",
    "spec": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc

@mcp.tool(name="read_doc_content",description="Read the contents of a document and return  it as a string.")
def read_doc_content(doc_id: str = Field(description="Id of the document to read")):
    if doc_id not in docs:
        raise ValueError(f"doc with id {doc_id} not found")
    
# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_a_document",
    description="Edit a document by replacing a string in the documents content with a new string"
)
def edit_docs(
    doc_id:str = Field(description="Id of the document that will be edited"),
    old_str : str = Field(description="the text to replace ,must match exactly,including whitesapace"),
    new_str:str = Field(description="the new text insert in place of the old text")
):
    if doc_id not in docs:
        raise ValueError(f"doct with id {doc_id} not found")
    
    docs[doc_id] = docs[doc_id].replace(old_str,new_str)

@mcp.tool(name="get_weather", description="Get the weather for a given city")
def get_weather(city:str):
    # implement weather logic here
    return f"Getting weather for: {city}"

mcp_app = mcp.streamable_http_app() # which transport use in this case streamable_http
