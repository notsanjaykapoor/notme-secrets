import dataclasses
import re
import typing

import sqlalchemy
import sqlmodel

import models
import services.mql


@dataclasses.dataclass
class Struct:
    code: int
    objects: typing.Sequence[models.ConvMsg]
    tags: list[str]
    count: int
    total: int
    errors: list[str]


def list(db_session: sqlmodel.Session, query: str = "", offset: int = 0, limit: int = 20, sort: str = "id+") -> Struct:
    """
    Search conv msgs table
    """
    struct = Struct(
        code=0,
        objects=[],
        tags=[],
        count=0,
        total=0,
        errors=[],
    )

    model = models.ConvMsg
    dataset = sqlmodel.select(model)  # default database query

    query_normalized = query

    if query and ":" not in query:
        query_normalized = f"id:{query}"

    struct_tokens = services.mql.parse(query_normalized)

    for token in struct_tokens.tokens:
        value = token["value"]

        if token["field"] == "conv_id":
            dataset = dataset.where(model.conv_id == int(value))
        elif token["field"] in ["id", "ids"]:
            values = [int(i) for i in value.split(",")]
            dataset = dataset.where(model.id.in_(values))  # ty: ignore
        elif token["field"] == "kind":
            # always like query
            value_normal = re.sub(r"~", "", value).lower()
            dataset = dataset.where(sqlalchemy.func.lower(model.kind).like("%" + value_normal + "%"))
        elif token["field"] in ["tags"]:
            values = [s.strip() for s in value.lower().split(",")]
            dataset = dataset.where(model.tags.contains(values))  # ty: ignore
            struct.tags = values

    dataset = dataset.offset(offset).limit(limit)

    if sort == "id+":
        dataset = dataset.order_by(model.id.asc())  # ty: ignore
    elif sort == "id-":
        dataset = dataset.order_by(model.id.desc())  # ty: ignore

    struct.objects = db_session.exec(dataset).all()
    struct.count = len(struct.objects)
    struct.total = db_session.scalar(sqlmodel.select(sqlalchemy.func.count("*")).select_from(dataset.subquery()))

    return struct
