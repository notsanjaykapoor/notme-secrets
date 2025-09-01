import sqlmodel

import models
import services.places.functions


def test_tool_match():
    queries_match = [
        "find fashion in paris",
        "find fashion in france",
        "find brand calmlence in paris",
        "find brand calmlence in france",
        "search fashion in belgium",
    ]

    for query in queries_match:
        code = services.places.functions.match_tool_use(query=query)
        assert code == 1

    queries_nomatch = [
        "web search fashion in paris",
    ]

    for query in queries_nomatch:
        code = services.places.functions.match_tool_use(query=query)
        assert code == 0
