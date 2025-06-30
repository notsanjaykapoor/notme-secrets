import services.database
import services.geo


def schemas() -> list[dict]:
    return [
        {
            "name": "maps_by_tag_city",
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

def maps_by_tag_city(location: str, tag: str) -> str:
    """
    """
    with services.database.session.get() as db_session:
        box = services.geo.get_by_name(db_session=db_session, name=location)

        if not box:
            return ""

        url = f"/geo/maps/box/{box.slug}"
        params = f"query=tags:{tag}"

        return f"{url}?{params}"
