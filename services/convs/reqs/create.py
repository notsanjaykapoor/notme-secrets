import typing

import sqlmodel

import models
import services.convs


def create(
    db_session: sqlmodel.Session, conv_id: int, request_id: str, state: str, user_id: int, data: dict = {}
) -> tuple[int, int, models.ConvReq | None]:
    """
    Create conversation request database object.
    """
    if conv_id == 0:
        # create conversation
        code, conv_db = services.convs.create(db_session=db_session, name=f"c-{request_id}", user_id=user_id, tags=[])
        if code != 0:
            return code, 0, None
        conv_id = typing.cast(int, conv_db.id)
    else:
        # use existing conversation
        pass

    conv_request_db = models.ConvReq(
        conv_id=conv_id,
        conv_msgs=[],
        data=data,
        request_id=request_id,
        state=state,
        user_id=user_id,
    )

    db_session.add(conv_request_db)
    db_session.commit()

    return 0, conv_id, conv_request_db
