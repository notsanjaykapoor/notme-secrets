import dataclasses

import services.mql

@dataclasses.dataclass
class Struct:
    tokens_match: list[dict]
    tokens_other: list[str]


def find(query: str, tokens: list[str], unquote: int = 0) -> Struct:
    """
    Find tokens in the specified query.  Returns matched tokens and non-matching tokens.
    
    :param query: search query
    :type query: str
    :param tokens: list of search tokens to look for
    :type tokens: list[str]
    :param unquote: 
    :type unquote: int
    :return: Description
    :rtype: Struct
    """
    struct = Struct([], [])

    parse_struct = services.mql.parse(query=query, unquote=unquote)

    for token in parse_struct.tokens:
        if (field := token["field"]) in tokens:
            struct.tokens_match.append(token)
        else:
            struct.tokens_other.append(f"{field}:{token["value"]}")

    return struct