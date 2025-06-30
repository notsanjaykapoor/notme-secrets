import models
import services.goog_places
import services.mapbox


def geo_search_by_name(city: models.City, name: str) -> tuple[int, list[dict]]:
    """
    Geo search place by name and location.
    """
    geo_list = services.goog_places.search_by_city(city=city, query=name)

    # if city.country_code in models.region.ASIA_EU_CODES:
    #     geo_list = services.goog_places.search_by_city(city=city, query=name)
    # else:
    #     geo_list = services.mapbox.search_by_city(city=city, query=name)

    return 0, geo_list
