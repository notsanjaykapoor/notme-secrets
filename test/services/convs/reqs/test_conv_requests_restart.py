import sqlmodel
import ulid

import models
import services.convs
import services.convs.reqs
import services.database


def test_conv_requests_restart(db_session: sqlmodel.Session, user_1: models.User):
    request_id = ulid.new().str

    # create conv request in cancelled state
    code, conv_id, req_db = services.convs.reqs.create(
        db_session=db_session,
        conv_id=0,
        data={},
        request_id=request_id,
        state=models.conv_req.STATE_CANCELLED,
        user_id=user_1.id,
    )

    assert code == 0
    assert conv_id
    assert req_db.id
    assert req_db.state == "cancelled"

    # should find 1 restartable conversation
    reqs_list = services.convs.reqs.restart_list(db_session=db_session)

    assert len(reqs_list) == 1

    services.database.truncate_tables(db_session=db_session, table_names=["conv_msgs", "conv_objs", "conv_reqs"])
