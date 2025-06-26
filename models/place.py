import datetime
import decimal

import sqlalchemy
import sqlalchemy.dialects.postgresql
import sqlmodel

class Place(sqlmodel.SQLModel, table=True):
    __tablename__ = "places"
    __table_args__ = (
        sqlalchemy.UniqueConstraint("name", name="i_place_name"),
        sqlalchemy.UniqueConstraint("source_id", "source_name", name="i_place_source"),
    )

    id: int = sqlmodel.Field(default=None, primary_key=True)

    brands: list[str] = sqlmodel.Field(
        default=[],
        sa_column=sqlmodel.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlmodel.String())),
    )
    city: str = sqlmodel.Field(index=True, nullable=False)
    country_code: str = sqlmodel.Field(index=True, nullable=False, max_length=5)
    data: dict = sqlmodel.Field(
        default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON)
    )
    geo_json: dict = sqlmodel.Field(
        default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON)
    )
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
    def brands_string(self) -> str:
        return ", ".join(self.brands)

    @property
    def city_country(self) -> str:
        return ", ".join([self.city, self.country_code])

    @property
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
    def notes(self) -> str:
        return self.data.get("notes", "")

    @property
    def notes_len(self) -> int:
        return len(self.data.get("notes", ""))

    @property
    def tags_string(self) -> str:
        return ", ".join(self.tags)