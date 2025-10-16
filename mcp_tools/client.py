import requests

url = 'http://localhost:8000/mcp'

headers = {
  'Accept': 'application/json,text/event-stream', #json ma response lega or sse events ma
}
  
body = {
  'jsonrpc': '2.0',
  'method': 'tools/call',
  'id': 1,
  "params": {
    "name": "read_document",
    "arguments": {
      "doc_id": "spec.txt"
    }
  }
}
  
      


response = requests.post(url,headers=headers , json=body)
print(response.text)