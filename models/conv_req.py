import datetime
import typing

import sqlalchemy
import sqlalchemy.dialects.postgresql
import sqlmodel

STATE_CANCELLED = "cancelled"
STATE_COMPLETED = "completed"
STATE_ERROR = "error"
STATE_PENDING = "pending"


class ConvReq(sqlmodel.SQLModel, table=True):
    __tablename__ = "conv_reqs"

    id: typing.Optional[int] = sqlmodel.Field(default=None, primary_key=True)

    created_at: datetime.datetime = sqlmodel.Field(
        sa_column=sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    conv_id: int = sqlmodel.Field(index=True, nullable=False)
    conv_msgs: list[int] = sqlmodel.Field(
        default=[],
        sa_column=sqlmodel.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlmodel.Integer())),
    )
    data: dict = sqlmodel.Field(default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON))
    request_id: str = sqlmodel.Field(index=True, nullable=False, max_length=100)
    state: str = sqlmodel.Field(index=True, nullable=False, max_length=30)
    updated_at: datetime.datetime = sqlmodel.Field(
        sa_column=sqlalchemy.Column(
            sqlalchemy.DateTime(timezone=True),
            nullable=False,
            onupdate=sqlalchemy.sql.func.now(),
        ),
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    user_id: int = sqlmodel.Field(index=True, nullable=False)
