import typing

import pydantic_ai.messages
import sqlmodel

import models
import services.convs.msgs


def load_by_conv_id(db_session: sqlmodel.Session, conv_id: int) -> tuple[int, list[pydantic_ai.messages.ModelMessage]]:
    """
    Load all conversation messages.
    """
    msgs_query = f"conv_id:{conv_id}"

    msgs_struct = services.convs.msgs.list(db_session=db_session, query=msgs_query, offset=0, limit=100, sort="id+")
    msgs_list = msgs_struct.objects

    return _load_msgs(msgs_list=msgs_list)


def _load_msgs(msgs_list: typing.Sequence[models.ConvMsg]) -> tuple[int, list[pydantic_ai.messages.ModelMessage]]:
    model_msgs = pydantic_ai.messages.ModelMessagesTypeAdapter.validate_python([msg.data for msg in msgs_list])

    return 0, model_msgs
