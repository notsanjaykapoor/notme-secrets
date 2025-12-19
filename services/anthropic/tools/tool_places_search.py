import sqlmodel

import models
import services.cities
import services.database
import services.geo


def schemas() -> list[dict]:
    return [
        {
            "name": "places_search_by_name_city",
            "description": "Search for places by name near a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city or the city and state, e.g. Chicago, IL or Tokyo",
                    },
                    "name": {
                        "type": "string",
                        "description": "The name of the place, e.g. 'pizza hut', 'atelier o'",
                    },
                },
                "required": ["location", "name"],
            },
        },
        {
            "name": "places_search_by_city",
            "description": "Search for places near a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city or the city and state, e.g. Chicago, IL or Tokyo",
                    },
                },
                "required": ["location"],
            },
        },
        {
            "name": "places_search_by_tag",
            "description": "Search for places by tag anywhere",
            "input_schema": {
                "type": "object",
                "properties": {
                    "tag": {
                        "type": "string",
                        "description": "The tag of the type of place, e.g. bar, fashion, food, hotel",
                    }
                },
                "required": ["tag"],
            },
        },
        {
            "name": "places_search_by_tag_city",
            "description": "Search for places by tag near a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city or the city and state, e.g. Chicago, IL or Tokyo",
                    },
                    "tag": {
                        "type": "string",
                        "description": "The tag of the type of place, e.g. bar, fashion, food, hotel",
                    },
                },
                "required": ["location", "tag"],
            },
        },
    ]


def places_search_by_name_city(location: str, name: str) -> str:
    """ """
    with services.database.session.get() as db_session:
        box = services.geo.get_by_name(db_session=db_session, name=location)

        if not box:
            return ""

        url = f"/geo/places/box/{box.slug}"
        params = f"query=name:{name}"

        return f"{url}?{params}"


def places_search_by_city(location: str) -> str:
    """ """
    with services.database.session.get() as db_session:
        box = _city_get_or_create(db_session=db_session, location=location)

        if not box:
            return ""

        return f"/geo/places/box/{box.slug}"


def places_search_by_tag(tag: str) -> str:
    """ """
    url = "/geo/places"
    params = f"query=tag:{tag}"

    return f"{url}?{params}"


def places_search_by_tag_city(location: str, tag: str) -> str:
    """ """
    with services.database.session.get() as db_session:
        box = services.geo.get_by_name(db_session=db_session, name=location)

        if not box:
            return ""

        url = f"/geo/places/box/{box.slug}"
        params = f"query=tag:{tag}"

        return f"{url}?{params}"


def _city_get_or_create(db_session: sqlmodel.Session, location: str) -> models.City | models.Region | None:
    box = services.geo.get_by_name(db_session=db_session, name=location)

    if box:
        return box

    code, box = services.cities.create(db_session=db_session, name=location)

    return box
