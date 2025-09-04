import datetime
import typing

import sqlalchemy
import sqlalchemy.dialects.postgresql
import sqlmodel


class ConvObj(sqlmodel.SQLModel, table=True):
    __tablename__ = "conv_objs"

    id: typing.Optional[int] = sqlmodel.Field(default=None, primary_key=True)

    created_at: datetime.datetime = sqlmodel.Field(
        sa_column=sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    data: dict = sqlmodel.Field(default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON))
    links: list[str] = sqlmodel.Field(
        default=[],
        sa_column=sqlmodel.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlmodel.String())),
    )
    name: str = sqlmodel.Field(index=False, nullable=True, default="")
    notes: str = sqlmodel.Field(
        default="",
        sa_column=sqlmodel.Column(sqlmodel.TEXT),
    )
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

    @property
    def notes_len(self) -> int:
        return len(self.notes)

    @property
    def tags_string(self) -> str:
        return ", ".join(self.tags)
