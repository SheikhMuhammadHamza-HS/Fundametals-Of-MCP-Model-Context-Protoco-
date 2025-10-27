from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR", stateless_http=True)

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.prompt()
async def hello_name(user_name:str):
    """ hello name function"""
    return f"my name is {user_name}"

@mcp.prompt()
def user_error_prompt(error:str):
    """ This function for error debugging """
    return [
        base.UserMessage(content='I am facing this error since morning...'),
        base.UserMessage(content=error),
        base.AssistantMessage(content=" let's try to debug the error")
        
    ]
    


mcp_app = mcp.streamable_http_app()