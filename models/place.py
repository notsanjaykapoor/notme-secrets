import datetime
import decimal
import re

import geoalchemy2
import geoalchemy2.shape
import pydantic
import shapely.geometry
import sqlalchemy
import sqlalchemy.dialects.postgresql
import sqlmodel

SOURCE_GOOGLE = "google"
SOURCE_MAPBOX = "mapbox"


class Place(sqlmodel.SQLModel, table=True):
    __tablename__ = "places"
    __table_args__ = (
        sqlalchemy.UniqueConstraint("name", name="i_place_name"),
        sqlalchemy.UniqueConstraint("source_id", "source_name", name="i_place_source"),
    )

    # enable arbitrary_types_allowed for pydantic v2 to handle ShapelyPoint
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    id: int = sqlmodel.Field(default=None, primary_key=True)

    brands: list[str] = sqlmodel.Field(
        default=[],
        sa_column=sqlmodel.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlmodel.String())),
    )
    city: str = sqlmodel.Field(index=True, nullable=False)
    country_code: str = sqlmodel.Field(index=True, nullable=False, max_length=5)
    data: dict = sqlmodel.Field(
        default_factory=dict,
        sa_column=sqlmodel.Column(sqlmodel.JSON),
    )
    geo_json: dict = sqlmodel.Field(
        default_factory=dict,
        sa_column=sqlmodel.Column(sqlmodel.JSON),
    )
    geom: shapely.geometry.Point = sqlmodel.Field(sa_column=sqlmodel.Column(geoalchemy2.Geometry("POINT", srid=4326)))
    lat: decimal.Decimal = sqlmodel.Field(max_digits=11, decimal_places=7, index=False, nullable=False)
    lon: decimal.Decimal = sqlmodel.Field(max_digits=11, decimal_places=7, index=False, nullable=False)
    name: str = sqlmodel.Field(index=True, nullable=False)
    source_id: str = sqlmodel.Field(index=False, nullable=True, default="")
    source_name: str = sqlmodel.Field(index=False, nullable=True, max_length=50, default="")
    tags: list[str] = sqlmodel.Field(
        default=[],
        sa_column=sqlmodel.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlmodel.String())),
    )
    updated_at: datetime.datetime = sqlmodel.Field(
        sa_column=sqlalchemy.Column(
            sqlalchemy.DateTime(timezone=True),
            nullable=False,
            onupdate=sqlalchemy.sql.func.now(),
        ),
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    user_id: int = sqlmodel.Field(index=True, nullable=False)
    website: str = sqlmodel.Field(index=False, nullable=True, default="")

    @property
    def brands_count(self) -> int:
        return len(self.brands)

    @property
    def brands_string(self) -> str:
        return ", ".join(self.brands)

    def brands_string_max(self, limit: int) -> str:
        return ", ".join(self.brands[0:limit])

        if len(self.brands) <= limit:
            return self.brands_string

        brands_str = ", ".join(self.brands[0:limit])
        brands_more = len(self.brands) - limit
        return f"{brands_str} +{brands_more}"

    @property
    def city_country(self) -> str:
        return ", ".join([self.city, self.country_code])

    @property
    def city_slug(self) -> str:
        return re.sub(r"\s", "-", self.city)

    def geo_json_compact(self, color: str) -> dict:
        return {
            "type": "Feature",
            "geometry": {
                "coordinates": [self.lon, self.lat],
                "type": "Point",
            },
            "properties": {
                "city": self.city,
                "color": color,
                "name": self.name,
            },
        }

    @property
    def lat_f(self) -> float:
        return float(self.lat)

    @property
    def lon_f(self) -> float:
        return float(self.lon)

    @property
    def notes(self) -> str:
        return self.data.get("notes", "")

    @notes.setter
    def notes(self, value: str):
        self.data = self.data | {"notes": value}

    @property
    def notes_len(self) -> int:
        return len(self.data.get("notes", ""))

    @property
    def point(self) -> shapely.geometry.Point:
        return geoalchemy2.shape.to_shape(self.geom)

    @property
    def tags_string(self) -> str:
        return ", ".join(self.tags)

    @property
    def tile_color(self) -> str:
        """color used by mapbox in tile view"""
        tags_set = set(self.tags)

        if tags_set.intersection(set(["bar", "cafe", "food"])):
            return "blue"
        elif tags_set.intersection(set(["hotel", "lodging", "rental"])):
            return "sky"
        elif tags_set.intersection(set(["clothing", "fashion", "shoes"])):
            return "orange"
        else:
            return "yellow"
