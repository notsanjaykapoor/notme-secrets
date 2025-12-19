import sqlmodel

import models


def get_by_id(db_session: sqlmodel.Session, id: int) -> models.ConvReq | None:
    db_select = sqlmodel.select(models.ConvReq).where(models.ConvReq.id == id)
    db_object = db_session.exec(db_select).first()

    return db_object


def get_by_request_id(db_session: sqlmodel.Session, request_id: str) -> models.ConvReq | None:
    db_select = sqlmodel.select(models.ConvReq).where(models.ConvReq.request_id == request_id)
    db_object = db_session.exec(db_select).first()

    return db_object
