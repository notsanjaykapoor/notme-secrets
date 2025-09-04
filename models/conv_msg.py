import datetime
import typing

import sqlalchemy
import sqlalchemy.dialects.postgresql
import sqlmodel


class ConvMsg(sqlmodel.SQLModel, table=True):
    __tablename__ = "conv_msgs"

    id: typing.Optional[int] = sqlmodel.Field(default=None, primary_key=True)

    conv_id: int = sqlmodel.Field(index=True, nullable=False)
    created_at: datetime.datetime = sqlmodel.Field(
        sa_column=sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    data: dict = sqlmodel.Field(default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON))
    kind: str = sqlmodel.Field(index=True, nullable=False, max_length=50)
    model_name: str = sqlmodel.Field(index=True, default="", nullable=True, max_length=100)
    parts_count: int = sqlmodel.Field(index=False, default=0)
    parts_names: list[str] = sqlmodel.Field(
        default=[],
        sa_column=sqlmodel.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlmodel.String())),
    )
    provider_name: str = sqlmodel.Field(index=True, default="", nullable=True, max_length=100)
    provider_response_id: str = sqlmodel.Field(index=False, default="", nullable=True, max_length=100)
    tags: list[str] = sqlmodel.Field(
        default=[],
        sa_column=sqlmodel.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlmodel.String())),
    )
    tools_map: dict = sqlmodel.Field(default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON))
    updated_at: datetime.datetime = sqlmodel.Field(
        sa_column=sqlalchemy.Column(
            sqlalchemy.DateTime(timezone=True),
            nullable=False,
            onupdate=sqlalchemy.sql.func.now(),
        ),
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    usage: dict = sqlmodel.Field(default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON))
    user_id: int = sqlmodel.Field(index=True, nullable=False)

    @property
    def tags_string(self) -> str:
        return ", ".join(self.tags)
