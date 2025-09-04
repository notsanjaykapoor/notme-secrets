import pydantic_ai.messages
import pydantic_core
import sqlmodel

import models
import services.convs.msgs


def persist(
    db_session: sqlmodel.Session, conv_id: int, user_id: int, model_msgs: list[pydantic_ai.messages.ModelMessage]
) -> tuple[int, list[models.ConvMsg]]:
    """
    Persist pydantic model messages to the database as conv msgs.

    The pydantic model messages are serialized to python dict before persisting.s
    """
    msgs_list = []

    json_list = pydantic_core.to_jsonable_python(model_msgs)

    for json_data in json_list:
        msg_db = services.convs.msgs.create(db_session, conv_id=conv_id, data=json_data, user_id=user_id, tags=[])
        msgs_list.append(msg_db)

    return 0, msgs_list
