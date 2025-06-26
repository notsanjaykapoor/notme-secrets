import services.anthropic.tools.tool_maps
import services.anthropic.tools.tool_places_search

def list() -> list[dict]:
    """
    Get list of claude tools.
    """
    tools_list = []

    schemas = [
        services.anthropic.tools.tool_maps.schemas(),
        services.anthropic.tools.tool_places_search.schemas(),
    ]

    for schema_list in schemas:
        tools_list.extend(schema_list)

    return tools_list
    