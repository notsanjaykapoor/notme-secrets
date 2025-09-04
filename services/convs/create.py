import sqlmodel

import models


def create(db_session: sqlmodel.Session, name: str, user_id: int, tags: list[str] = []) -> tuple[int, models.ConvObj]:
    """
    Create conversation database object.
    """
    conv_obj_db = models.ConvObj(
        name=name,
        tags=sorted(tags),
        user_id=user_id,
    )

    db_session.add(conv_obj_db)
    db_session.commit()

    return 0, conv_obj_db
