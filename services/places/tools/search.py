import pydantic_ai

import services.database
import services.places

def search_by_city(ctx: pydantic_ai.RunContext[str], city: str, brands: list[str]=[], tags: list[str]=[]) -> dict[str, int | dict]:
    """
    Search the places database by city to find places of interest, especially fashion stores and restaurants.

    args:
        city: city name, e.g. berlin, paris
        brands: optional list of brand names
        tags: optional list of tags, e.g. 'fashion', 'restaurant'
    """
    query = f"city:{city.lower()}"

    if brands:
        brands_str = ",".join([s.lower() for s in brands if s])
        query = f"brands:{brands_str}"

    if tags:
        tags_str = ",".join([s.lower() for s in tags if s])
        query = f"tags:{tags_str}"

    return _list_by_query(query=query)


def search_by_country(ctx: pydantic_ai.RunContext[str], country: str, brands: list[str]=[], tags: list[str]=[]) -> dict[str, int | dict]:
    """
    Search the places database by country to find places of interest, especially fashion stores and restaurants.

    args:
        country: The country code in 2 letter format.
        brands: optional list of brand names
        tags: optional list of tags, e.g. 'fashion', 'restaurant'
    """
    country_normal = country.lower()
    tags_str = ",".join([s.lower() for s in tags if s])

    return _list_by_query(query=f"country_code:{country_normal} tags:{tags_str}")


def _list_by_query(query: str, offset: int = 0, limit: int = 50, sort: str = "name+") -> dict[str, int | dict]:
    with services.database.session.get() as db_session:
        places_struct = services.places.list(
            db_session=db_session,
            query=query,
            offset=offset,
            limit=limit,
            sort=sort,
        )

        places_list = [place.as_dict() for place in places_struct.objects]

        return {
            "places": places_list,
            "total": places_struct.total,
        }
