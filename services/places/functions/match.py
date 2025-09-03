import re

import sqlmodel

import services.places.tags


def match_tool_use(db_session: sqlmodel.Session, query: str) -> int:
    """
    Returns 1 if query looks like a places tool signature, 0 otherwise.
    """

    if re.search(r"web search", query):
        return 0

    tags_set = services.places.tags.list_all(
        db_session=db_session,
        box=None,
    )

    tags_re = "|".join(list(tags_set))

    if re.search(r"find|search", query) and re.search(rf"{tags_re}", query):
        return 1

    return 0
