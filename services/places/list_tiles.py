import models


def list_tiles(places: list[models.Place], color: str) -> list[dict]:
    """
    Convert list of places to list of tiles that can be consumed by mapbox.
    """
    tiles = []
 
    for place in places:
      tile = {
        "type": "Feature",
        "geometry": {
            "coordinates": [float(place.lon), float(place.lat)],
            "type": "Point",
        },
        "properties": {
            "city": place.city,
            "color": color,
            "name": place.name,
        }
      }

      tiles.append(tile)

    return tiles
