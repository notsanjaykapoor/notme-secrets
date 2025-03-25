import typing

import sqlmodel

import models


def create(
    db_session: sqlmodel.Session,
    name: str,
    user_id: int,
    uri: str,
    categories: list[str] = [],
) -> typing.Optional[models.Bookmark]:
    """
    Create bookmark and persist to database
    """

    bm = models.Bookmark(
        categories=categories,
        name=name.lower().strip(),
        user_id=user_id,
        uri=uri,
    )

    db_session.add(bm)
    db_session.commit()

    return bm


