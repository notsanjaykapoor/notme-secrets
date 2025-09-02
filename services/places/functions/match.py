import re

import services.places.tags


def match_tool_use(query: str) -> int:
    """
    Returns 1 if query looks like a places tool signature, 0 otherwise.
    """

    if re.search(r"web search", query):
        return 0

    if re.search(r"find|search", query) and re.search(r"brand|fashion|hotel|places|restaurants?", query):
        # if re.search(r"find|search fashion|hotel|places|restaurants?", query):
        return 1

    return 0
