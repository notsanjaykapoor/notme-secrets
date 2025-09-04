import pydantic_ai.messages
import sqlmodel

import models
import services.convs
import services.convs.msgs
import services.database


msg_1_request = {
    "parts": [
        {
            "content": "You are a helpful agent.",
            "timestamp": "2025-09-03T15:18:46.694238Z",
            "dynamic_ref": None,
            "part_kind": "system-prompt",
        },
        {
            "content": "hi",
            "timestamp": "2025-09-03T15:18:46.694242Z",
            "part_kind": "user-prompt",
        },
    ],
    "instructions": None,
    "kind": "request",
}


msg_1_response = {
    "parts": [
        {
            "content": "Hello! I'm here to help you with any questions or tasks you might have. I have access to web search capabilities, so I can help you research information online if needed. What would you like to know or do today?",
            "part_kind": "text",
        }
    ],
    "usage": {
        "input_tokens": 475,
        "cache_write_tokens": 0,
        "cache_read_tokens": 0,
        "output_tokens": 49,
        "input_audio_tokens": 0,
        "cache_audio_read_tokens": 0,
        "output_audio_tokens": 0,
        "details": {
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
            "input_tokens": 475,
            "output_tokens": 49,
        },
    },
    "model_name": "claude-sonnet-4-20250514",
    "timestamp": "2025-09-03T15:18:48.558144Z",
    "kind": "response",
    "provider_name": "anthropic",
    "provider_details": None,
    "provider_response_id": "msg_01McFp61kMiRmAdnk3hkYntx",
}


def test_convs_msgs_load_request(db_session: sqlmodel.Session, user_1: models.User, conv_1: models.ConvObj):
    code, msg_1 = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_1.id,
        data=msg_1_request,
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert msg_1.id

    code, model_msgs_list = services.convs.msgs.load_by_conv_id(db_session=db_session, conv_id=conv_1.id)

    assert code == 0
    assert len(model_msgs_list) == 1

    model_msg = model_msgs_list[0]

    assert isinstance(model_msg, pydantic_ai.messages.ModelRequest)

    services.database.truncate_tables(db_session=db_session, table_names=["conv_msgs"])


def test_convs_msgs_load_response(db_session: sqlmodel.Session, user_1: models.User, conv_1: models.ConvObj):
    code, msg_1 = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_1.id,
        data=msg_1_response,
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert msg_1.id

    code, model_msgs_list = services.convs.msgs.load_by_conv_id(db_session=db_session, conv_id=conv_1.id)

    assert code == 0
    assert len(model_msgs_list) == 1

    model_msg = model_msgs_list[0]

    assert isinstance(model_msg, pydantic_ai.messages.ModelResponse)

    services.database.truncate_tables(db_session=db_session, table_names=["conv_msgs"])
