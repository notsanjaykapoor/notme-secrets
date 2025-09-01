import models


def list_tiles(places: list[models.Place]) -> list[dict]:
    """
    Convert list of places to list of tiles that can be consumed by mapbox.
    """
    tiles = []

    for place in places:
        tile = {
            "type": "Feature",
            "geometry": {
                "coordinates": [place.lon_f, place.lat_f],
                "type": "Point",
            },
            "properties": {
                "city": place.city,
                "color": place.tile_color,
                "country": place.country_code,
                "name": place.name,
            },
        }

        tiles.append(tile)

    return tiles
