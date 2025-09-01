import sqlalchemy
import sqlmodel

import models


def count_by_key(db_session: sqlmodel.Session, key_id: int) -> int:
    """
    Return count of secrets with key_id
    """
    model = models.Secret
    dataset = sqlmodel.select(model).where(model.key_id == key_id)

    return db_session.scalar(sqlmodel.select(sqlalchemy.func.count("*")).select_from(dataset.subquery()))
