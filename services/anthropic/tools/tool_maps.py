def schemas() -> list[dict]:
    return [
        {
            "name": "maps_by_tag",
            "description": "Show map of tags near a location",
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

def maps_by_tag(location: str, tag: str):
    """
    """
