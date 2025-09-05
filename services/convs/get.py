import sqlmodel

import models


def get_by_id(db_session: sqlmodel.Session, id: int) -> models.ConvObj | None:
    db_select = sqlmodel.select(models.ConvObj).where(models.ConvObj.id == id)
    db_object = db_session.exec(db_select).first()

    return db_object
