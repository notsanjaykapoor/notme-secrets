import pydantic_ai

import services.tools.anthropic
import services.tools.parallel


def list() -> list[pydantic_ai.Tool]:
    """
    List all available tools
    """
    return [
        pydantic_ai.Tool(services.tools.anthropic.anth_search, takes_ctx=True),
        # pydantic_ai.Tool(services.tools.parallel.par_search, takes_ctx=True),
        # pydantic_ai.Tool(services.places.functions.list_by_tags_city, takes_ctx=False),
    ]
