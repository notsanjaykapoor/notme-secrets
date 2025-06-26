import datetime
import decimal

import sqlalchemy
import sqlalchemy.dialects.postgresql
import sqlmodel

class Region(sqlmodel.SQLModel, table=True):
    __tablename__ = "regions"
    __table_args__ = (sqlalchemy.UniqueConstraint("name", name="i_region_name"),)

    id: int = sqlmodel.Field(default=None, primary_key=True)

    bbox: list[float] = sqlmodel.Field(
        default=[],
        sa_column=sqlmodel.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlmodel.Float())),
    )
    country_code: str = sqlmodel.Field(index=False, nullable=True, max_length=5, default="")
    data: dict = sqlmodel.Field(
        default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON)
    )
    geo_json: dict = sqlmodel.Field(
        default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON)
    )
    lat: decimal.Decimal = sqlmodel.Field(max_digits=11, decimal_places=7, index=False, nullable=False)
    lon: decimal.Decimal = sqlmodel.Field(max_digits=11, decimal_places=7, index=False, nullable=False)
    name: str = sqlmodel.Field(index=True, nullable=False)
    slug: str = sqlmodel.Field(index=True, nullable=False)
    source_id: str = sqlmodel.Field(index=False, nullable=True, max_length=100, default="")
    source_name: str = sqlmodel.Field(index=False, nullable=True, max_length=50, default="")
    tags: list[str] = sqlmodel.Field(
        default=[],
        sa_column=sqlmodel.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlmodel.String())),
    )
    type: str = sqlmodel.Field(index=False, nullable=True, max_length=50, default="")
    updated_at: datetime.datetime = sqlmodel.Field(
        sa_column=sqlalchemy.Column(
            sqlalchemy.DateTime(timezone=True),
            nullable=False,
            onupdate=sqlalchemy.sql.func.now(),
        ),
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )


    @property
    def lon_max(self) -> float:
        return self.bbox[3]

    @property
    def lon_min(self) -> float:
        return self.bbox[2]

    @property
    def lat_max(self) -> float:
        return self.bbox[1]

    @property
    def lat_min(self) -> float:
        return self.bbox[0]

    @property
    def map_zoom(self) -> int:
        if self.type == "country":
            return 8
        if self.type == "continent":
            return 4
        else:
            return 4
