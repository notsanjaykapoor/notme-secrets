import models
import services.goog_places


def geo_search_by_name(box: models.City | models.Region, name: str) -> tuple[int, list[dict]]:
    """
    Geo search place by name and location.
    """
    if box.type == models.box.TYPE_CITY:
        geo_list = services.goog_places.search_by_city(city=box, query=name)
    else: # region, todo
        geo_list = []

    return 0, geo_list
