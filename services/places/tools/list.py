import pydantic_ai

import services.places.tools.search

def list() -> list[pydantic_ai.Tool]:
    return [
        pydantic_ai.Tool(services.places.tools.search.search_by_city, takes_ctx=True),
        pydantic_ai.Tool(services.places.tools.search.search_by_country, takes_ctx=True),
    ]
