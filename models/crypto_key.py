import os
import typing

import sqlalchemy
import sqlmodel


LOCATION_DEFAULT = f"file://{os.path.expanduser('~')}/.gnupg/"

NAME_DEFAULT = "notme-default"

TYPE_GPG_SYM = "gpg-sym"
TYPE_KMS_SYM = "kms-sym"  # google kms

class CryptoKey(sqlmodel.SQLModel, table=True):
    __tablename__ = "crypto_keys"
    __table_args__ = (sqlalchemy.UniqueConstraint("name", "user_id", name="_crypto_key_name_user"),)

    id: typing.Optional[int] = sqlmodel.Field(default=None, primary_key=True)

    data: dict = sqlmodel.Field(
        default_factory=dict, sa_column=sqlmodel.Column(sqlmodel.JSON)
    )
    name: str = sqlmodel.Field(index=True, nullable=False)
    location: str = sqlmodel.Field(index=False, nullable=False)
    type: str = sqlmodel.Field(index=True, nullable=False)
    user_id: int = sqlmodel.Field(index=True, nullable=False)

