import dataclasses
import re

import sqlalchemy
import sqlmodel

import models
import services.mql


@dataclasses.dataclass
class Struct:
    code: int
    objects: list[models.Place]
    brands: list[str]
    tags: list[str]
    count: int
    total: int
    errors: list[str]


def list(
    db_session: sqlmodel.Session, query: str = "", offset: int = 0, limit: int = 20, sort: str="id+"
) -> Struct:
    """
    Search places table
    """
    struct = Struct(
        code=0,
        objects=[],
        brands=[],
        tags=[],
        count=0,
        total=0,
        errors=[],
    )

    model = models.Place
    dataset = sqlmodel.select(model)  # default database query

    query_normalized = query

    if query and ":" not in query:
        query_normalized = f"name:{query}"

    struct_tokens = services.mql.parse(query_normalized)

    for token in struct_tokens.tokens:
        value = token["value"]

        if token["field"] in ["brand", "brands"]:
            values = [s.strip() for s in value.lower().split(",")]
            dataset = dataset.where(model.brands.contains(values))
            struct.brands = values
        elif token["field"] == "city":
            # always like query
            value_normal = re.sub(r"~", "", value).lower()
            dataset = dataset.where(
                sqlalchemy.func.lower(model.city).like("%" + value_normal + "%")
            )
        elif token["field"] == "name":
            # always like query
            value_normal = re.sub(r"~", "", value).lower()
            dataset = dataset.where(
                sqlalchemy.func.lower(model.name).like("%" + value_normal + "%")
            )
        elif token["field"] == "source_id":
            dataset = dataset.where(model.source_id == value)
        elif token["field"] == "source_name":
            dataset = dataset.where(model.source_name == value)
        elif token["field"] in ["tag", "tags"]:
            values = [s.strip() for s in value.lower().split(",")]
            dataset = dataset.where(model.tags.contains(values))
            struct.tags = values
        elif token["field"] in ["uid", "user_id"]:
            dataset = dataset.where(model.user_id == int(value))

    db_query = dataset.offset(offset).limit(limit)

    if sort == "id+":
        db_query = db_query.order_by(model.id.asc())
    elif sort == "id-":
        db_query = db_query.order_by(model.id.desc())
    elif sort == "name+":
        db_query = db_query.order_by(model.name.asc())
    elif sort == "name-":
        db_query = db_query.order_by(model.name.desc())
    else: # default is "id+"
        db_query = db_query.order_by(model.id.asc())

    struct.objects = db_session.exec(db_query).all()
    struct.count = len(struct.objects)
    struct.total = db_session.scalar(
        sqlmodel.select(sqlalchemy.func.count("*")).select_from(dataset.subquery())
    )

    return struct