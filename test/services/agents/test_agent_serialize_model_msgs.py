import pydantic_core
import sqlmodel

import datetime
from pydantic_ai.messages import BuiltinToolCallPart, BuiltinToolReturnPart, ModelResponse, RequestUsage, TextPart
from anthropic.types.beta import BetaWebSearchResultBlock

import models
import services.agents
import services.convs.msgs

model_response_1 = ModelResponse(
    parts=[
        BuiltinToolCallPart(
            tool_name="web_search",
            args={"query": "fashion trends US 2025"},
            tool_call_id="srvtoolu_013yusBggrYvwrWpeg5w5GcF",
            provider_name="anthropic",
        ),
        BuiltinToolReturnPart(
            tool_name="web_search_tool_result",
            content=[
                BetaWebSearchResultBlock(
                    encrypted_content="",
                    page_age="July 2, 2025",
                    title="2025 Fashion Trends: Top 10 Forecasted Trends",
                    type="web_search_result",
                    url="https://heuritech.com/fashion-trends-2025/",
                ),
                BetaWebSearchResultBlock(
                    encrypted_content="",
                    page_age="March 24, 2025",
                    title="9 Fashion Trends Defining 2025: Capes To Bubble Skirts",
                    type="web_search_result",
                    url="https://www.refinery29.com/en-us/fashion-trends-2025",
                ),
                BetaWebSearchResultBlock(
                    encrypted_content="",
                    page_age="3 days ago",
                    title="Fall 2025’s Biggest Fashion Trends, According to Editors",
                    type="web_search_result",
                    url="https://www.cosmopolitan.com/style-beauty/fashion/a65783064/fall-fashion-trend-report-2025/",
                ),
                BetaWebSearchResultBlock(
                    encrypted_content="",
                    page_age="March 19, 2025",
                    title="The 2025 Fashion Trends Taking Shape in Real Time | Marie Claire",
                    type="web_search_result",
                    url="https://www.marieclaire.com/fashion/fashion-trends-2025/",
                ),
                BetaWebSearchResultBlock(
                    encrypted_content="",
                    page_age="2 days ago",
                    title="Fall 2025 Fashion Trends You Can Wear Now | Marie Claire",
                    type="web_search_result",
                    url="https://www.marieclaire.com/fashion/fall-2025-fashion-trends/",
                ),
                BetaWebSearchResultBlock(
                    encrypted_content="",
                    page_age="1 week ago",
                    title="6 Best Fall 2025 Fashion Trends to Shop Now",
                    type="web_search_result",
                    url="https://www.today.com/shop/best-fall-2025-fashion-trends-rcna226161",
                ),
                BetaWebSearchResultBlock(
                    encrypted_content="",
                    page_age="2 weeks ago",
                    title="These 7 Fashion Trends Will Be Huge Come Fall 2025 | Who What Wear",
                    type="web_search_result",
                    url="https://www.whowhatwear.com/fashion/shopping/fashion-trends-fall-2025",
                ),
                BetaWebSearchResultBlock(
                    encrypted_content="",
                    page_age="March 6, 2025",
                    title="10 Must-Know US Fashion Retail Industry Trends for 2025",
                    type="web_search_result",
                    url="https://www.scayle.com/library/blog/us-fashion-industry-trends/",
                ),
                BetaWebSearchResultBlock(
                    encrypted_content="",
                    page_age="January 17, 2025",
                    title="2025 Fashion Trends For Women over 60: What's In, What's Out",
                    type="web_search_result",
                    url="https://awellstyledlife.com/2025-fashion-trends-whats-in-whats-out-and-how-to-stay-stylish/",
                ),
                BetaWebSearchResultBlock(
                    encrypted_content="",
                    page_age="May 22, 2025",
                    title="The Top Summer 2025 Trends, According to Fashion Power Players | Marie Claire",
                    type="web_search_result",
                    url="https://www.marieclaire.com/fashion/summer-2025-fashion-trends/",
                ),
            ],
            tool_call_id="srvtoolu_013yusBggrYvwrWpeg5w5GcF",
            timestamp=datetime.datetime(2025, 9, 5, 18, 14, 33, 56735, tzinfo=datetime.timezone.utc),
            provider_name="anthropic",
        ),
        TextPart(
            content="Based on my search results, here are the key fashion trends shaping the US in 2025:\n\n## Spring/Summer 2025 Trends\n\n**Aquatic/Mermaid-Core Aesthetic**\n"
        ),
        TextPart(
            content="Fashion is diving into aquatic influences with turquoise colors forecasted to increase by +8% and mermaid-inspired elements like sequins and fishtail maxi dresses expected to grow by +20% and +17% respectively"
        ),
        TextPart(content=". "),
        TextPart(
            content="This includes glamour, sequins, fishtail skirts paired with sporty elements like fishnet jogger pants and scuba-inspired looks"
        ),
        TextPart(content=".\n\n**Power Leg/Asymmetrical Silhouettes**\n"),
        TextPart(
            content='Spring/Summer 2025 is being called the "season of the power leg," with designers creating hybrid pants-shorts combinations and asymmetrical silhouettes that showcase just one leg'
        ),
        TextPart(content=".\n\n**Hot Pants Revival**\n"),
        TextPart(
            content="Hot pants have emerged as the new alternative to mini skirts, with a forecasted +7% increase in popularity from April to June 2025 and +14% increase from July to September, particularly embraced by Gen Z consumers"
        ),
        TextPart(content=".\n\n**Sheer and Flowing Fabrics**\n"),
        TextPart(
            content="Designers are building entire collections around fluid, diaphanous fabrics with gossamer-light silks, twisted tulle skirts, and sheer overdresses taking center stage"
        ),
        TextPart(content=".\n\n## Fall 2025 Trends\n\n**Pattern Mixing**\n"),
        TextPart(
            content='Pattern mixing has reached "delightfully chaotic levels" with designers proving that plaids, stripes, and florals can all coexist in one look, suggesting there might not be such a thing as clashing anymore'
        ),
        TextPart(content=".\n\n**Bohemian Chic Evolution**\n"),
        TextPart(
            content="Boho chic is making a polished comeback, moving beyond last season's rugged vintage vibe to emphasize romantic, feminine silhouettes that feel effortless yet intentional"
        ),
        TextPart(content=".\n\n**Faux Fur and Texture**\n"),
        TextPart(
            content="Faux fur is trending not just for coats but for stoles and even bra tops, with the trend focusing on texture piled on top of more texture to add depth and interest to layered outfits"
        ),
        TextPart(content=".\n\n**Sports-Inspired Elements**\n"),
        TextPart(
            content="Sports-inspired attire is popular for transitional months, with track shorts paired with chunky sweaters, side-striped pants with heels, and rugby crewnecks as key pieces"
        ),
        TextPart(content=".\n\n## Color Trends\n\n"),
        TextPart(
            content='For 2025, expect "superimposed pastels" including blues with quiet charm and bouncy mints with fizzy freshness, balanced by a unique blend of grey and beige for simplicity and stability'
        ),
        TextPart(content=".\n\n## Accessories and Footwear\n\n"),
        TextPart(
            content='Classic Mary Jane and Oxford shoes are trending, with searches for these styles rising and Pinterest showing a +5,597% increase in searches for "preppy vibes" over the last year'
        ),
        TextPart(content=".\n\n"),
        TextPart(
            content="Wedges are making a controversial comeback, but this time they're sculptural with unexpected silhouettes in flashy materials like patent leather"
        ),
        TextPart(content=".\n\n## Overall Philosophy\n\n"),
        TextPart(
            content='The modern fashion approach has shifted from "see now, wear six months later" to "see now and wear tonight," with consumers cutting back on impulse purchases and demanding multitasking clothes that transition seamlessly from weekend to boardroom'
        ),
        TextPart(content=".\n\n"),
        TextPart(
            content='The overarching mantra for 2025 is "meaningful minimalism" - pieces with thoughtful and functional details that do more with less'
        ),
        TextPart(content="."),
    ],
    usage=RequestUsage(
        input_tokens=18084,
        output_tokens=1102,
        details={
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
            "input_tokens": 18084,
            "output_tokens": 1102,
        },
    ),
    model_name="claude-sonnet-4-20250514",
    timestamp=datetime.datetime(2025, 9, 5, 18, 14, 33, 56936, tzinfo=datetime.timezone.utc),
    provider_name="anthropic",
    provider_response_id="msg_01GEg1KdbBPXmzoKw6WQjcAA",
)


def test_serialize_model_msgs(db_session: sqlmodel.Session, user_1: models.User, conv_1: models.ConvObj):
    json_list = pydantic_core.to_jsonable_python([model_response_1])
    assert json_list

    json_list = services.agents.serialize_model_msgs(model_msgs=[model_response_1])

    code, msgs_list = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_1.id,
        data_list=json_list,
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert len(msgs_list) == 1

    msg_db = msgs_list[0]
    assert msg_db.id
    assert msg_db.data == json_list[0]
    assert msg_db.kind == "response"
    assert msg_db.provider_name == "anthropic"
