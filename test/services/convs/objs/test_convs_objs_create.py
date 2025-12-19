import sqlmodel
import ulid

import models
import services.convs
import services.database


def test_convs_objs_create(db_session: sqlmodel.Session, user_1: models.User):
    conv_name = f"c-{ulid.new().str}"
    code, conv_db = services.convs.create(db_session=db_session, name=conv_name, user_id=user_1.id)

    assert code == 0
    assert conv_db.id
    assert conv_db.name == conv_name

    services.database.truncate_tables(db_session=db_session, table_names=["conv_objs"])
