import sqlmodel
import ulid

import models
import services.convs
import services.convs.msgs
import services.convs.reqs
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


def test_conv_requests_create(db_session: sqlmodel.Session, user_1: models.User):
    request_id = ulid.new().str

    # create conv object and request
    code, conv_id, req_db = services.convs.reqs.create(
        db_session=db_session,
        conv_id=0,
        data={
            "user_prompt": "hey",
        },
        request_id=request_id,
        state=models.conv_req.STATE_PENDING,
        user_id=user_1.id,
    )

    assert code == 0

    conv_db = services.convs.get_by_id(db_session=db_session, id=conv_id)

    assert conv_db.id
    assert req_db.conv_id == conv_id
    assert req_db.data == {"user_prompt": "hey"}
    assert req_db.request_id == request_id
    assert req_db.state == "pending"

    # simulate agent run to generates messages

    code, msgs_list = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_db.id,
        data_list=[msg_1_basic],
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert len(msgs_list) == 1

    msg_1 = msgs_list[0]
    assert msg_1.id
    assert msg_1.conv_id == conv_db.id

    # update conv request

    services.convs.reqs.update_state(
        db_session=db_session,
        request_id=request_id,
        state_from=models.conv_req.STATE_PENDING,
        state_to=models.conv_req.STATE_COMPLETED,
        conv_msg_ids=[msg_1.id],
    )

    req_db = services.convs.reqs.get_by_request_id(db_session=db_session, request_id=request_id)

    assert req_db.conv_msgs == [msg_1.id]
    assert req_db.state == "completed"

    services.database.truncate_tables(db_session=db_session, table_names=["conv_msgs", "conv_objs", "conv_reqs"])
