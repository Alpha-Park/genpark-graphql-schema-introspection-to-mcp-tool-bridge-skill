"""MCP server for GraphQL Schema Introspection to MCP Tool Bridge."""
import sys
import json
from client import GraphQLToMCPBridge

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "convert_graphql_to_mcp",
                "description": "Converts GraphQL field definitions into MCP tool schemas",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "graphql_fields": {"type": "array"}
                    },
                    "required": ["graphql_fields"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "convert_graphql_to_mcp":
            fields = params.get("arguments", {}).get("graphql_fields", [])
            res = GraphQLToMCPBridge.convert_fields_to_mcp(fields)
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
