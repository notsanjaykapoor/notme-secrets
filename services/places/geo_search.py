import models
import services.geoapify
import services.goog_places
import services.mapbox


def geo_search_by_name(city: models.City, name: str) -> tuple[int, list[dict]]:
    """
    Geo search place by name and location.
    """
    if city.country_code == "jp":
        geo_list = services.goog_places.search_by_city(city=city, query=name)
    else:
        geo_list = services.mapbox.search_by_city(city=city, query=name)

    return 0, geo_list
