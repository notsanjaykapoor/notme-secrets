import sqlmodel

import services.convs.msgs


def delete_by_id(db_session: sqlmodel.Session, id: int) -> tuple[int, list[int]]:
    """
    Delete conversation and all related messages.

    Returns tuple with status code and list of deleted message ids.
    """
    conv_db = services.convs.get_by_id(db_session=db_session, id=id)

    if not conv_db:
        return [404, []]

    msgs_query = f"conv_id:{id}"
    msgs_struct = services.convs.msgs.list(db_session=db_session, query=msgs_query, offset=0, limit=1024)
    msgs_list = msgs_struct.objects

    msg_ids = []
    for msg_db in msgs_list:
        db_session.delete(msg_db)
        msg_ids.append(msg_db.id)

    db_session.delete(conv_db)
    db_session.commit()

    return 0, msg_ids
