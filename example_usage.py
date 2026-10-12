"""Example usage for GraphQL Schema Introspection to MCP Tool Bridge."""
from client import GraphQLToMCPBridge

if __name__ == "__main__":
    fields = [
        {"name": "createIssue", "operation_type": "mutation", "args": [{"name": "title", "type": "String!"}, {"name": "priority", "type": "Int"}]}
    ]
    res = GraphQLToMCPBridge.convert_fields_to_mcp(fields)
    print("Converted Tools:", res["tools"])
