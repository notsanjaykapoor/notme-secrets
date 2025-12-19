import sqlmodel

import models
import services.convs
import services.convs.msgs
import services.database


msg_1_basic = {
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

msg_2_basic = {
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


def test_convs_msgs_create_basic(db_session: sqlmodel.Session, user_1: models.User, conv_1: models.ConvObj):
    code, msgs_list = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_1.id,
        data_list=[msg_1_basic],
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert len(msgs_list) == 1

    msg_1 = msgs_list[0]
    assert msg_1.created_at
    assert msg_1.id
    assert msg_1.kind == "request"
    assert msg_1.parts_count == 2
    assert msg_1.parts_names == ["system-prompt", "user-prompt"]

    code, msgs_list = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_1.id,
        data_list=[msg_2_basic],
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert code == 0
    assert len(msgs_list) == 1

    msg_2 = msgs_list[0]
    assert msg_2.id
    assert msg_2.kind == "response"
    assert msg_2.model_name == "claude-sonnet-4-20250514"
    assert msg_2.parts_count == 1
    assert msg_2.parts_names == ["text"]
    assert msg_2.provider_name == "anthropic"
    assert msg_2.provider_response_id == "msg_01McFp61kMiRmAdnk3hkYntx"
    assert msg_2.usage

    services.database.truncate_tables(db_session=db_session, table_names=["conv_msgs"])
