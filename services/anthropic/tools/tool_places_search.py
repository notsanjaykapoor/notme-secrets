

def schemas() -> list[dict]:
    return [
        {
            "name": "places_search_by_name",
            "description": "Search for places by name near a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city or the city and state, e.g. Chicago, IL or Tokyo"
                    },
                    "name": {
                        "type": "string",
                        "description": "The name of the place, e.g. 'pizza hut', 'atelier o'"
                    }
                },
                "required": ["location", "name"]
            }
        },
        {
            "name": "places_search_by_tag",
            "description": "Search for places tagged with a specific value near a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city or the city and state, e.g. Chicago, IL or Tokyo"
                    },
                    "tag": {
                        "type": "string",
                        "description": "The tag of the place, e.g. bar, fashion, food, hotel"
                    }
                },
                "required": ["location", "tag"]
            }
        },
    ]


def places_search_by_name(location: str, name: str):
    """
    """


def places_search_by_tag(location: str, tag: str):
    """
    """

