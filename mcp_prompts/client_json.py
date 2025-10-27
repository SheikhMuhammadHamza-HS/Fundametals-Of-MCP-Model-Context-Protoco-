import requests


url = 'http://localhost:8000/mcp'
header = {
  'Accept': 'application/json,text/event-stream'
}

# return a list of available prompts
body = {
  "jsonrpc": "2.0",
  "id": 1,
  "method": "prompts/list",
  "params": {}
}

# get a specific prompt with arguments
body = {
  "jsonrpc": "2.0",
  "id": 1,
  "method": "prompts/get",
  "params": {
    'name': 'user_error_prompt',
    'arguments': {
      'error': 'python Error'
    }
  }
}

response = requests.post(headers=header,json=body,url=url)
print(response.text)