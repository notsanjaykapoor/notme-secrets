import sqlmodel

import models
import services.convs
import services.convs.msgs
import services.database


msg_1_tool = {
    "parts": [
        {
            "content": "You are a helpful agent.",
            "timestamp": "2025-09-03T15:38:43.952316Z",
            "dynamic_ref": None,
            "part_kind": "system-prompt",
        },
        {
            "content": "web search fashion in paris",
            "timestamp": "2025-09-03T15:38:43.952320Z",
            "part_kind": "user-prompt",
        },
    ],
    "instructions": None,
    "kind": "request",
}

msg_2_tool = {
    "parts": [
        {
            "content": "I'll search for information about fashion in Paris for you.",
            "part_kind": "text",
        },
        {
            "tool_name": "parallel_ai_search",
            "args": {
                "objective": "Find information about fashion in Paris, including current trends, fashion districts, shopping areas, designers, and fashion scene",
                "search_queries": [
                    "Paris fashion trends 2024",
                    "Paris fashion districts shopping",
                    "Paris haute couture designers",
                    "Paris fashion week",
                    "best fashion stores Paris",
                ],
            },
            "tool_call_id": "toolu_01Rc4uQeh77va88XtgArAvKM",
            "part_kind": "tool-call",
        },
    ],
    "usage": {
        "input_tokens": 480,
        "cache_write_tokens": 0,
        "cache_read_tokens": 0,
        "output_tokens": 137,
        "input_audio_tokens": 0,
        "cache_audio_read_tokens": 0,
        "output_audio_tokens": 0,
        "details": {
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
            "input_tokens": 480,
            "output_tokens": 137,
        },
    },
    "model_name": "claude-sonnet-4-20250514",
    "timestamp": "2025-09-03T15: 38: 47.034783Z",
    "kind": "response",
    "provider_name": "anthropic",
    "provider_details": None,
    "provider_response_id": "msg_01GmLwFXLQmve176bhmgZTiE",
}

msg_3_tool = {
    "parts": [
        {
            "tool_name": "parallel_ai_search",
            "content": [
                {
                    "url": "https://parisjetaime.com/eng/article/paris-shopping-districts-a821",
                    "title": "Paris shopping districts - Office de Tourisme de Paris",
                    "excerpts": [
                        "\\nhopping-a821 )\\n* [![Deutsch](/public/images/otcp/icon/flag_DE.svg)](https://parisjetaime.com/ger/artikel/quartiers-parisiens-ou-faire-son-shopping-a821 Deutsch)\\n* [![Espa\\u00f1ol](/public/images/otcp/icon/flag_ES.svg)](https://parisjetaime.com/spa/articulo/barrios-parisinos-donde-ir-de-compras-a821 Espa)\\n\\n![Image](https://parisjetaime.com/data/layout_image/33869_IMG_9012%20Shopping%20rue%20Legendre%20%C2%A9%20Studio%20TTG_panoramic_2-1_xs.JPG?ver=1700703323)\\n\\nShopping\\n\\n# Paris shopping districts\\n\\nNo doubt about it, Paris is definitely the fashion capital\\n\\nParisians dress a variety of styles, from chic and haute couture to bohemian and trendy, and there is an equal variety of places to go shopping depending on what you\\u2019re looking for. Here are the most sought-after shopping districts in Paris.\\n\\n## The Golden Triangle: a must-do\\n\\n![Image](https://parisjetaime.com/data/layout_image/6658_Avenue-des-Champs-%C3%89lys%C3%A9es-Pi%C3%A9tons-11--630x405--%C2%A9-Sarah-Cantaloube.jpg) "
                    ],
                }
            ],
            "tool_call_id": "toolu_01Rc4uQeh77va88XtgArAvKM",
            "metadata": None,
            "timestamp": "2025-09-03T15:38:49.274529Z",
            "part_kind": "tool-return",
        }
    ],
    "instructions": None,
    "kind": "request",
}

msg_4_tool = {
    "parts": [
        {
            "content": "Based on my web search, here's what I found about fashion in Paris:\n\n## Paris Fashion Scene\n\n**Paris is undoubtedly the fashion capital of the world**, offering everything from haute couture to trendy street style. The city provides diverse shopping experiences for all budgets and tastes.\n\n## Top Fashion Districts & Shopping Areas\n\n### **The Golden Triangle** (8th Arrondissement)\n- **Avenue Montaigne**: Home to Chanel, Dior, and other luxury maisons\n- **Champs-Élysées**: Famous shopping avenue with both luxury and mainstream brands\n- **Avenue des Champs-Élysées**: Mix of flagship stores and tourist-friendly shops\n\n### **Saint-Germain-des-Prés** (6th Arrondissement)\n- **Boulevard Saint-Germain**: Sophisticated boutiques and designer stores\n- **Rue du Bac**: Known for Le Bon Marché, Paris's oldest department store\n- Bohemian chic and intellectual fashion vibe\n\n### **Le Marais** (3rd & 4th Arrondissements)\n- Trendy boutiques and vintage stores\n- Mix of emerging designers and established brands\n- Great for unique, artisanal fashion finds\n\n### **Place Vendôme** (1st Arrondissement)\n- Ultra-luxury jewelry and haute couture\n- Home to prestigious fashion houses\n\n## Current Fashion Trends (2024)\n\nFrench women are embracing several key trends:\n1. **Pops of Red** - Strategic red accents in accessories and clothing\n2. **Loafers with Socks** - Classic Parisian chic\n3. **Trench Coats** - Timeless French elegance\n4. **Denim Trends** - Updated classic cuts\n5. **Quiet Luxury** - Understated elegance over flashy logos\n\n## Paris Fashion Week\n\n- **Next Season**: Spring/Summer 2026 (September 29 - October 7, 2025)\n- Features both ready-to-wear and haute couture collections\n- Major international fashion event showcasing French and international designers\n\n## Famous French Fashion Designers\n\nParis is home to legendary fashion houses including:\n- **Chanel**\n- **Dior**\n- **Louis Vuitton** \n- **Hermès**\n- **Saint Laurent**\n- **Givenchy**\n\n## Shopping Tips\n\n- **Department Stores**: Galeries Lafayette and Printemps for variety\n- **Sales Periods**: Semi-annual sales offer great deals on luxury items\n- **Hidden Gems**: Explore 19th-century shopping passages and arcades\n- **Local Style**: Parisians favor quality over quantity, classic pieces over trends\n\nParis offers an unparalleled fashion experience, from window shopping along the Champs-Élysées to discovering emerging designers in the Marais!",
            "part_kind": "text",
        }
    ],
    "usage": {
        "input_tokens": 4336,
        "cache_write_tokens": 0,
        "cache_read_tokens": 0,
        "output_tokens": 660,
        "input_audio_tokens": 0,
        "cache_audio_read_tokens": 0,
        "output_audio_tokens": 0,
        "details": {
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
            "input_tokens": 4336,
            "output_tokens": 660,
        },
    },
    "model_name": "claude-sonnet-4-20250514",
    "timestamp": "2025-09-03T15:39:05.530981Z",
    "kind": "response",
    "provider_name": "anthropic",
    "provider_details": None,
    "provider_response_id": "msg_01Tq8YLNY9ZVKbXt2PzdEpGN",
}


def test_convs_msgs_create_tool(db_session: sqlmodel.Session, user_1: models.User, conv_1: models.ConvObj):
    code, msgs_list = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_1.id,
        data_list=[msg_1_tool],
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert len(msgs_list) == 1

    msg_1 = msgs_list[0]
    assert msg_1.id
    assert msg_1.kind == "request"

    code, msgs_list = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_1.id,
        data_list=[msg_2_tool],
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert len(msgs_list) == 1

    msg_2 = msgs_list[0]
    assert msg_2.id
    assert msg_2.kind == "response"
    assert msg_2.model_name == "claude-sonnet-4-20250514"
    assert msg_2.parts_count == 2
    assert msg_2.parts_names == ["text", "tool-call"]
    assert msg_2.provider_name == "anthropic"
    assert msg_2.provider_response_id == "msg_01GmLwFXLQmve176bhmgZTiE"
    assert msg_2.tools_map == {"toolu_01Rc4uQeh77va88XtgArAvKM": "parallel_ai_search"}
    assert msg_2.usage

    code, msgs_list = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_1.id,
        data_list=[msg_3_tool],
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert len(msgs_list) == 1

    msg_3 = msgs_list[0]
    assert msg_3.id
    assert msg_3.kind == "request"
    assert msg_3.parts_count == 1
    assert msg_3.parts_names == ["tool-return"]
    assert msg_3.tools_map == {"toolu_01Rc4uQeh77va88XtgArAvKM": "parallel_ai_search"}

    code, msgs_list = services.convs.msgs.create(
        db_session=db_session,
        conv_id=conv_1.id,
        data_list=[msg_4_tool],
        user_id=user_1.id,
        tags=[],
    )

    assert code == 0
    assert len(msgs_list) == 1

    msg_4 = msgs_list[0]
    assert msg_4.id
    assert msg_4.kind == "response"
    assert msg_4.parts_count == 1
    assert msg_4.parts_names == ["text"]
    assert msg_4.provider_name == "anthropic"
    assert msg_4.provider_response_id == "msg_01Tq8YLNY9ZVKbXt2PzdEpGN"
    assert msg_4.tools_map == {}
    assert msg_4.usage

    services.database.truncate_tables(db_session=db_session, table_names=["conv_msgs"])
