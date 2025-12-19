import sqlmodel

import models
import services.convs
import services.convs.msgs
import services.database


msg_1_function = {
    "parts": [
        {
            "content": "You are a helpful agent. Use one of the following tools if possible to help compose your answer.",
            "timestamp": "2025-09-03T15:35:39.005873Z",
            "dynamic_ref": None,
            "part_kind": "system-prompt",
        },
        {"content": "find fashion in paris", "timestamp": "2025-09-03T15: 35: 39.005877Z", "part_kind": "user-prompt"},
    ],
    "instructions": None,
    "kind": "request",
}

msg_2_function = {
    "parts": [
        {
            "tool_name": "final_result_list_by_tags_city",
            "args": {"city": "Paris", "tags": ["fashion"]},
            "tool_call_id": "pyd_ai_3e1fc982020c4b1fa4997f7378772256",
            "part_kind": "tool-call",
        }
    ],
    "usage": {
        "input_tokens": 330,
        "cache_write_tokens": 0,
        "cache_read_tokens": 0,
        "output_tokens": 15,
        "input_audio_tokens": 0,
        "cache_audio_read_tokens": 0,
        "output_audio_tokens": 0,
        "details": {"text_prompt_tokens": 330, "text_candidates_tokens": 15},
    },
    "model_name": "gemini-1.5-flash",
    "timestamp": "2025-09-03T15: 35: 44.370009Z",
    "kind": "response",
    "provider_name": "google-gla",
    "provider_details": {"finish_reason": "STOP"},
    "provider_response_id": "S2C4aLGhDauM_PUP0I3uwQk",
}

msg_3_function = {
    "parts": [
        {
            "tool_name": "final_result_list_by_tags_city",
            "content": "Final result processed.",
            "tool_call_id": "pyd_ai_3e1fc982020c4b1fa4997f7378772256",
            "metadata": None,
            "timestamp": "2025-09-03T15:35:44.456501Z",
            "part_kind": "tool-return",
        }
    ],
    "instructions": None,
    "kind": "request",
}


def test_convs_msgs_create_function(db_session: sqlmodel.Session, user_1: models.User, conv_1: models.ConvObj):
    code, msgs_list = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_1.id,
        data_list=[msg_1_function],
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert len(msgs_list) == 1

    msg_1 = msgs_list[0]
    assert msg_1.id
    assert msg_1.kind == "request"

    code, msgs_list = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_1.id,
        data_list=[msg_2_function],
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert len(msgs_list) == 1

    msg_2 = msgs_list[0]
    assert msg_2.id
    assert msg_2.kind == "response"
    assert msg_2.model_name == "gemini-1.5-flash"
    assert msg_2.parts_count == 1
    assert msg_2.parts_names == ["tool-call"]
    assert msg_2.provider_name == "google-gla"
    assert msg_2.provider_response_id == "S2C4aLGhDauM_PUP0I3uwQk"
    assert msg_2.tools_map == {"pyd_ai_3e1fc982020c4b1fa4997f7378772256": "final_result_list_by_tags_city"}

    code, msgs_list = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_1.id,
        data_list=[msg_3_function],
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert len(msgs_list) == 1

    msg_3 = msgs_list[0]
    assert msg_3.id
    assert msg_3.kind == "request"
    assert msg_3.parts_count == 1
    assert msg_3.parts_names == ["tool-return"]
    assert msg_3.tools_map == {"pyd_ai_3e1fc982020c4b1fa4997f7378772256": "final_result_list_by_tags_city"}

    services.database.truncate_tables(db_session=db_session, table_names=["conv_msgs"])
