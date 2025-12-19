import pydantic_ai.messages
import pydantic_core
import sqlmodel

import models
import services.agents
import services.convs.msgs


def persist(
    db_session: sqlmodel.Session, conv_id: int, user_id: int, model_msgs: list[pydantic_ai.messages.ModelMessage]
) -> tuple[int, list[models.ConvMsg]]:
    """
    Persist pydantic model messages to the database as conv msgs.

    The pydantic model messages are serialized to a python dict before persisting
    """
    try:
        json_list = pydantic_core.to_jsonable_python(model_msgs)
    except Exception as e:
        # see this occasionally - TypeError: 'MockValSer' object cannot be converted to 'SchemaSerializer'
        # use the fallback serializer
        json_list = services.agents.serialize_model_msgs(model_msgs=model_msgs)

    code, msgs_list = services.convs.msgs.create(
        db_session, conv_id=conv_id, data_list=json_list, user_id=user_id, tags=[]
    )

    return code, msgs_list
