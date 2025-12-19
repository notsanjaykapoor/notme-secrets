import typing

import sqlmodel

import services.convs.reqs


def update_state(
    db_session: sqlmodel.Session,
    request_id: str,
    state_from: typing.Literal["pending"],
    state_to: typing.Literal["cancelled", "completed", "error"],
    conv_msg_ids: list[int | None],
) -> int:
    req_db = services.convs.reqs.get_by_request_id(db_session=db_session, request_id=request_id)

    if not req_db:
        return 404

    if req_db.state != state_from:
        return 422

    req_db.conv_msgs = conv_msg_ids
    req_db.state = state_to

    db_session.add(req_db)
    db_session.commit()

    return 0
