import models
import services.database
import services.places


def list_by_brands_anywhere(brands: list[str]) -> dict[list[models.Place], int]:
    """
    Search places by brand.

    Args:
      brands: List of brands.

    Returns:
        dict: A dictionary containing places data:
            - 'places': list of matching places
            - 'total': total number of matching places
    """
    brands_str = ",".join([s.lower() for s in brands if s])

    return _list_by_query(query=f"brands:{brands_str}")


def list_by_brands_city(city: str, brands: list[str]) -> dict[list[models.Place], int]:
    """
    Search places by city and brand.

    Args:
      city: The city name.
      brands: List of brands.

    Returns:
        dict: A dictionary containing places data:
            - 'places': list of matching places
            - 'total': total number of matching places
    """
    city_normal = city.lower()
    brands_str = ",".join([s.lower() for s in brands if s])

    return _list_by_query(query=f"city:{city_normal} brands:{brands_str}")


def list_by_brands_country(country: str, brands: list[str]) -> dict[list[models.Place], int]:
    """
    Search places by country and tags.

    Args:
      country: The country code in 2 letter format.
      brands: List of brands.

    Returns:
        dict: A dictionary containing places data:
            - 'places': list of matching places
            - 'total': total number of matching places
    """
    country_normal = country.lower()
    brands_str = ",".join([s.lower() for s in brands if s])

    return _list_by_query(query=f"country_code:{country_normal} brands:{brands_str}")


def list_by_tags_city(city: str, tags: list[str]) -> dict[list[models.Place], int]:
    """
    Search places by city and tags.

    Args:
        city: The city name.
        tags: List of tags.

    Returns:
        dict: A dictionary containing places data:
            - 'places': list of matching places
            - 'total': total number of matching places
    """
    city_normal = city.lower()
    tags_str = ",".join([s.lower() for s in tags if s])

    return _list_by_query(query=f"city:{city_normal} tags:{tags_str}")


def list_by_tags_country(country: str, tags: list[str]) -> dict[list[models.Place], int]:
    """
    Search places by country and tags.

    Args:
      country: The country code in 2 letter format.
      tags: List of tags.

    Returns:
        dict: A dictionary containing places data:
            - 'places': list of matching places
            - 'total': total number of matching places
    """
    country_normal = country.lower()
    tags_str = ",".join([s.lower() for s in tags if s])

    return _list_by_query(query=f"country_code:{country_normal} tags:{tags_str}")


def _list_by_query(query: str, offset: int = 0, limit: int = 50, sort: str = "name+") -> dict[list[models.Place], int]:
    with services.database.session.get() as db_session:
        places_struct = services.places.list(
            db_session=db_session,
            query=query,
            offset=offset,
            limit=limit,
            sort=sort,
        )

        return {
            "places": places_struct.objects,
            "total": places_struct.total,
        }


# def _output_markdown(places: list[models.Place]) -> str:
#     """
#     Convert list of models to markdown text
#     """

#     md_list = []

#     md_list.append(f"found {len(places)} places:\n\n")

#     for place in places:
#         md_list.append(f"**{place.name}, {place.city}**\n")

#         if place.brands_count > 0:
#             md_list.append(f"- brands: {place.brands_string}\n")

#         if place.website:
#             md_list.append(f"- website: {place.website}\n")

#         md_list.append("\n")

#     return "".join(md_list)
