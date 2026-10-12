"""GraphQL Schema Introspection to MCP Tool Bridge.
100% Python Standard Library.
"""

class GraphQLToMCPBridge:
    """Converts GraphQL query and mutation field definitions into MCP tool JSON Schema specifications."""

    @staticmethod
    def convert_fields_to_mcp(graphql_fields: list) -> dict:
        tools = []
        for field in graphql_fields:
            f_name = field.get("name", "query_field")
            op_type = field.get("operation_type", "query").lower()
            desc = field.get("description", f"Executes GraphQL {op_type} {f_name}")
            args = field.get("args", [])

            props = {}
            required = []
            for a in args:
                a_name = a.get("name", "arg")
                gql_type = a.get("type", "String")
                is_req = gql_type.endswith("!")
                clean_type = gql_type.rstrip("!").lower()
                json_type = "integer" if clean_type == "int" else ("number" if clean_type == "float" else ("boolean" if clean_type == "boolean" else "string"))
                props[a_name] = {"type": json_type}
                if is_req:
                    required.append(a_name)

            tools.append({
                "name": f"gql_{op_type}_{f_name}",
                "description": f"[GraphQL {op_type.upper()}] {desc}",
                "inputSchema": {
                    "type": "object",
                    "properties": props,
                    "required": required
                }
            })

        return {
            "converted_tools_count": len(tools),
            "tools": tools
        }
