import typing

import pydantic_ai

import services.database
import services.places

async def search_by_city(ctx: pydantic_ai.RunContext[str], city: str, brands: list[str]=[], tags: list[str]=[]) -> dict[str, typing.Any]:
    """
    Search the places database by city to find places of interest, especially fashion stores and restaurants.
    The brands and tags args are optional.  If specified, they are used to filter the search results.

    args:
        city: city name, e.g. berlin, paris
        brands: optional list of brand names
        tags: optional list of tags, e.g. 'fashion', 'restaurant'
    """
    query = f"city:{city.lower()}"

    if brands:
        brands_norm = _brands_filter(brands=brands)
        brands_str = ",".join([s.lower() for s in brands_norm if s])
        query = f"{query} brands:{brands_str}"

    if tags:
        tags_norm = _tags_filter(tags=tags)
        tags_str = ",".join([s.lower() for s in tags_norm if s])
        query = f"{query} tags:{tags_str}"

    return await _list_by_query(query=query)


async def search_by_country(ctx: pydantic_ai.RunContext[str], country: str, brands: list[str]=[], tags: list[str]=[]) -> dict[str, typing.Any]:
    """
    Search the places database by country to find places of interest, especially fashion stores and restaurants.
    The brands and tags args are optional.  If specified, they are used to filter the search results.

    args:
        country: The country code in 2 letter format.
        brands: optional list of brand names
        tags: optional list of tags, e.g. 'fashion', 'restaurant'
    """
    query = f"country_code:{country.lower()}"

    if brands:
        brands_norm = _brands_filter(brands=brands)
        brands_str = ",".join([s.lower() for s in brands_norm if s])
        query = f"{query} brands:{brands_str}"

    if tags:
        tags_norm = _tags_filter(tags=tags)
        tags_str = ",".join([s.lower() for s in tags_norm if s])
        query = f"{query} tags:{tags_str}"

    return await _list_by_query(query=query)


async def _list_by_query(query: str, offset: int = 0, limit: int = 50, sort: str = "name+") -> dict[str, typing.Any]:
    with services.database.session.get() as db_session:
        places_struct = services.places.list(
            db_session=db_session,
            query=query,
            offset=offset,
            limit=limit,
            sort=sort,
        )

        # convert place db object to a serializable dict
        places_list: list[dict] = [place.as_dict() for place in places_struct.objects]

        return {
            "places": places_list,
            "total": places_struct.total,
        }


def _brands_filter(brands: list[str]) -> list[str]:
    """Filter brands to remove improperly formatted brands"""
    return [brand.lower() for brand in brands if (" " not in brand)]


def _tags_filter(tags: list[str]) -> list[str]:
    """Filter tags to remove improperly formatted brands"""
    return [tag.lower() for tag in tags if (" " not in tag)]