import requests

url = "http://localhost:8000/mcp/"

headers = {
  "Accept" : "application/json,text/event-stream", # response in json and streaming
}

# body = {
#   "jsonrpc": "2.0", #jsonrpc version
#   "method": "tools/list", # run on  tools on the server
#   "id": "1", # id of the request
#   "params": {}, #paramteres for the method
# }
body = {
  "jsonrpc": "2.0", 
  "method": "tools/list", 
  "id": "1", 
  "params": {
    "name": "read_doc_content",
    "arguments": {
      "doc_id": "deposition.md"
    }
  }, 
}


response = requests.post(url,headers=headers,json=body)
print(response.text)
