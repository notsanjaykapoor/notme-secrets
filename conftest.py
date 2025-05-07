import os

import pytest
import sqlalchemy
import sqlalchemy.future
import sqlmodel
import sqlmodel.pool

import dot_init  # noqa: F401
import models
import services.database

# set env vars
os.environ["APP_ENV"] = "tst"
os.environ["KMS_KEY_TEST"] = "kms:projects/notme-330419/locations/us-central1/keyRings/ring-tst/cryptoKeys/tst-1"

test_db_name = os.environ.get("DATABASE_TEST_URL")
connect_args: dict = {}

assert test_db_name

if "sqlite" in test_db_name:
    # sqlite specific
    connect_args = {"check_same_thread": False}

engine = sqlmodel.create_engine(
    test_db_name,
    connect_args=connect_args,
    poolclass=sqlmodel.pool.StaticPool,
)


def database_tables_create(engine: sqlalchemy.future.Engine):
    sqlmodel.SQLModel.metadata.create_all(engine)


def database_tables_drop(engine: sqlalchemy.future.Engine):
    sqlmodel.SQLModel.metadata.drop_all(engine)


# Set up the database once
database_tables_drop(engine)
database_tables_create(engine)


@pytest.fixture(name="db_session")
def session_fixture():
    connection = engine.connect()
    transaction = connection.begin()

    # begin a nested transaction (using SAVEPOINT)
    nested = connection.begin_nested()

    session = sqlmodel.Session(engine)

    # if the application code calls session.commit, it will end the nested transaction
    # when that happens, start a new one.
    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    # yield session to test
    yield session

    session.close()

    # rollback the overall transaction, restoring the state before the test ran
    transaction.rollback()
    connection.close()


@pytest.fixture(name="bm_1")
def bookmark_1_fixture(db_session: sqlmodel.Session, user_1: models.User):
    bm = models.Bookmark(
        categories=["category-1"],
        name="bookmark-1",
        tags=["tag-1"],
        user_id=user_1.id,
        uri="https://www.google.com",
    )

    db_session.add(bm)
    db_session.commit()

    assert bm.id

    yield bm

    services.database.truncate_tables(db_session=db_session, table_names=["bookmarks"])


@pytest.fixture(name="key_gpg_1")
def crypto_key_gpg_1_fixture(db_session: sqlmodel.Session, user_1: models.User):
    key = models.CryptoKey(
        location="file:///me/you",
        name="gpg-1",
        type=models.crypto_key.TYPE_GPG_SYM,
        user_id=user_1.id,
    )

    db_session.add(key)
    db_session.commit()

    assert key.id

    yield key

    services.database.truncate_tables(db_session=db_session, table_names=["crypto_keys"])


@pytest.fixture(name="key_gpg_me")
def crypto_key_gpg_me_fixture(db_session: sqlmodel.Session, user_1: models.User):
    key = models.CryptoKey(
        location=models.crypto_key.LOCATION_DEFAULT,
        name="gpg-me",
        type=models.crypto_key.TYPE_GPG_SYM,
        user_id=user_1.id,
    )

    db_session.add(key)
    db_session.commit()

    assert key.id

    yield key

    services.database.truncate_tables(db_session=db_session, table_names=["crypto_keys"])


@pytest.fixture(name="key_kms_1")
def crypto_key_kms_1_fixture(db_session: sqlmodel.Session, user_1: models.User):
    key = models.CryptoKey(
        location=os.environ.get("KMS_KEY_TEST"),
        name="kms-1",
        type=models.crypto_key.TYPE_KMS_SYM,
        user_id=user_1.id,
    )

    db_session.add(key)
    db_session.commit()

    assert key.id

    yield key

    services.database.truncate_tables(db_session=db_session, table_names=["crypto_keys"])


@pytest.fixture(name="user_1")
def user_1_fixture(db_session: sqlmodel.Session):
    user = models.User(
        data={},
        email="user-1@gmail.com",
        idp=models.user.IDP_GOOGLE,
        state=models.user.STATE_ACTIVE,
    )

    db_session.add(user)
    db_session.commit()

    assert user.id

    yield user

    services.database.truncate_tables(db_session=db_session, table_names=["users"])
