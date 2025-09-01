import models
import services.database
import services.places


def list_all() -> list:
    return [
        list_by_brands_anywhere,
        list_by_brands_city,
        list_by_brands_country,
        list_by_tags_city,
        list_by_tags_country,
    ]


def list_by_brands_anywhere(brands: list[str]) -> list[models.Place]:
    """
    Search places by brand.

    Args:
      brands: List of brands.

    Returns:
        list of places.
    """
    brands_str = ",".join([s.lower() for s in brands if s])

    return _list_by_query(query=f"brands:{brands_str}")


def list_by_brands_city(city: str, brands: list[str]) -> list[models.Place]:
    """
    Search places by city and brand.

    Args:
      city: The city name.
      brands: List of brands.

    Returns:
        list of places.
    """
    city_normal = city.lower()
    brands_str = ",".join([s.lower() for s in brands if s])

    return _list_by_query(query=f"city:{city_normal} brands:{brands_str}")


def list_by_brands_country(country: str, brands: list[str]) -> list[models.Place]:
    """
    Search places by country and tags.

    Args:
      country: The country code in 2 letter format.
      brands: List of brands.

    Returns:
        list of places.
    """
    country_normal = country.lower()
    brands_str = ",".join([s.lower() for s in brands if s])

    return _list_by_query(query=f"country_code:{country_normal} brands:{brands_str}")


def list_by_tags_city(city: str, tags: list[str]) -> list[models.Place]:
    """
    Search places by city and tags.

    Args:
      city: The city name.
      tags: List of tags.

    Returns:
        list of places.
    """
    city_normal = city.lower()
    tags_str = ",".join([s.lower() for s in tags if s])

    return _list_by_query(query=f"city:{city_normal} tags:{tags_str}")


def list_by_tags_country(country: str, tags: list[str]) -> list[models.Place]:
    """
    Search places by country and tags.

    Args:
      country: The country code in 2 letter format.
      tags: List of tags.

    Returns:
        list of places.
    """
    country_normal = country.lower()
    tags_str = ",".join([s.lower() for s in tags if s])

    return _list_by_query(query=f"country_code:{country_normal} tags:{tags_str}")


def _list_by_query(query: str, offset: int = 0, limit: int = 50, sort: str = "name+") -> list[models.Place]:
    with services.database.session.get() as db_session:
        places_struct = services.places.list(
            db_session=db_session,
            query=query,
            offset=offset,
            limit=limit,
            sort=sort,
        )

        return [place for place in places_struct.objects]
