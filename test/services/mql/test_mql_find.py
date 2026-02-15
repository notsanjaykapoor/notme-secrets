import services.mql

def test_mql_find():
    query_basic = "tags:foo"
    query_with_near = "tags:foo near:paris"

    struct = services.mql.find(query=query_basic, tokens=["near"])

    assert struct.tokens_match == []
    assert struct.tokens_other == ["tags:foo"]

    struct = services.mql.find(query=query_with_near, tokens=["near"])

    assert struct.tokens_match == [{"field": "near", "value": "paris"}]
    assert struct.tokens_other == ["tags:foo"]