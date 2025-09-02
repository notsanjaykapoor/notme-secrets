import pydantic_ai

import services.places.functions


def list_outputs() -> list:
    return [
        services.places.functions.list_by_brands_anywhere,
        services.places.functions.list_by_brands_city,
        services.places.functions.list_by_brands_country,
        services.places.functions.list_by_tags_city,
        services.places.functions.list_by_tags_country,
    ]


def list_tools() -> list[pydantic_ai.Tool]:
    return [pydantic_ai.Tool(services.places.functions.list_by_tags_city, takes_ctx=False)]
