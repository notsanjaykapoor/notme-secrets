import pydantic_ai

import services.agents.tools


def list() -> list[pydantic_ai.Tool]:
    """
    List all available tools
    """
    return [
        pydantic_ai.Tool(services.agents.tools.parallel_search, takes_ctx=False),
        # pydantic_ai.Tool(services.places.functions.list_by_tags_city, takes_ctx=False),
    ]
