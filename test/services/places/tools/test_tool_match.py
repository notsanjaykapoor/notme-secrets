import sqlmodel

import services.places.functions


def test_tool_match(db_session: sqlmodel.Session):
    queries_match = [
        "find fashion in paris",
        "find fashion in france",
        "find brand calmlence in paris",
        "find brand calmlence in france",
        "search fashion in belgium",
    ]

    for query in queries_match:
        code = services.places.functions.match_tool_use(db_session=db_session, query=query)
        assert code == 1

    queries_nomatch = [
        "web search fashion in paris",
    ]

    for query in queries_nomatch:
        code = services.places.functions.match_tool_use(db_session=db_session, query=query)
        assert code == 0
