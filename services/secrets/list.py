import dataclasses
import re

import sqlalchemy
import sqlmodel

import models
import services.mql


@dataclasses.dataclass
class Struct:
    code: int
    objects: list[models.Secret]
    tags: list[str]
    count: int
    total: int
    errors: list[str]


def list(
    db_session: sqlmodel.Session, query: str = "", offset: int = 0, limit: int = 20, scope: str="", sort: str="name+",
) -> Struct:
    """
    Search bookmarks table
    """
    struct = Struct(
        code=0,
        objects=[],
        tags=[],
        count=0,
        total=0,
        errors=[],
    )

    model = models.Secret
    dataset = sqlmodel.select(model)  # default database query

    query_normalized = query

    if query and ":" not in query:
        query_normalized = f"name:{query}"

    if scope:
        query_normalized = f"{query_normalized} {scope}".strip()

    struct_tokens = services.mql.parse(query_normalized)

    for token in struct_tokens.tokens:
        value = token["value"]

        if token["field"] in ["key_id"]:
            dataset = dataset.where(model.key_id == int(value))
        elif token["field"] == "name":
            # always like query
            value_normal = re.sub(r"~", "", value).lower()
            dataset = dataset.where(
                sqlalchemy.func.lower(model.name).like("%" + value_normal + "%")
            )
        elif token["field"] in ["tags"]:
            values = [s.strip() for s in value.lower().split(",")]
            dataset = dataset.where(model.tags.contains(values))
            struct.tags = values
        elif token["field"] in ["uid", "user_id"]:
            dataset = dataset.where(model.user_id == int(value))

    db_query = dataset.offset(offset).limit(limit)

    if sort == "name+":
        db_query = db_query.order_by(model.name.asc())
    elif sort == "name-":
        db_query = db_query.order_by(model.name.desc())
    else: # default is "name+"
        db_query = db_query.order_by(model.name.asc())

    struct.objects = db_session.exec(db_query).all()
    struct.count = len(struct.objects)
    struct.total = db_session.scalar(
        sqlmodel.select(sqlalchemy.func.count("*")).select_from(dataset.subquery())
    )

    return struct