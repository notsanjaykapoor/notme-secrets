import typing

import sqlalchemy
import sqlalchemy.dialects.postgresql
import sqlmodel


class Secret(sqlmodel.SQLModel, table=True):
    __tablename__ = "secrets"
    __table_args__ = (sqlalchemy.UniqueConstraint("name", "user_id", name="_secrets_user_name"),)

    id: typing.Optional[int] = sqlmodel.Field(default=None, primary_key=True)

    data: dict = sqlmodel.Field(default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON))
    data_cipher: str = sqlmodel.Field(
        sa_column=sqlmodel.Column(sqlmodel.TEXT, nullable=False),
    )
    key_id: int = sqlmodel.Field(index=True, nullable=False)
    name: str = sqlmodel.Field(index=True, nullable=True)
    tags: list[str] = sqlmodel.Field(
        default=[],
        sa_column=sqlmodel.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlmodel.String())),
    )
    user_id: int = sqlmodel.Field(index=True, nullable=False)
