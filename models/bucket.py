import typing

import sqlalchemy
import sqlmodel


class Bucket(sqlmodel.SQLModel, table=True):
    __tablename__ = "buckets"
    __table_args__ = (sqlalchemy.UniqueConstraint("name", "user_id", name="_bucket_user_name"),)

    id: typing.Optional[int] = sqlmodel.Field(default=None, primary_key=True)

    data: dict = sqlmodel.Field(default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON))
    name: str = sqlmodel.Field(index=True, nullable=True)
    location: str = sqlmodel.Field(index=False, nullable=True)
    user_id: int = sqlmodel.Field(index=True, nullable=False)
