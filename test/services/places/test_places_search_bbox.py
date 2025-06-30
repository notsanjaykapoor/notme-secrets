import shapely.geometry
import sqlmodel
import ulid

import models
import services.database
import services.places



def test_places_search_bbox():
    points = [
        (1, 2),
        {3, 4},
        (2, 1),
    ]

    polygon = shapely.Polygon(points)
    
    assert polygon.bounds == (1.0, 1.0, 3.0, 4.0)
