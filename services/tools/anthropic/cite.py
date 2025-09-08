import json
import os

import httpx
import pydantic_ai

import services.anthropic

url = "https://api.anthropic.com/v1/messages"


async def anth_cite(
    context: pydantic_ai.RunContext[str],
    query: str,
    doc: services.anthropic.DocCustom | services.anthropic.DocPdf | services.anthropic.DocText,
) -> dict:
    """
    Use anthropic with citations enabled.

    Args:
        query: The query string for the search.
        doc: Document to cite.

    Returns:
        A list of search results containing type, text, and citations.
    """
    # generate content params
    content = [
        {
            "type": "text",
            "text": query,
        }
    ]

    if isinstance(doc, services.anthropic.DocText):
        content.append(
            {
                "citations": {"enabled": True},
                "source": {
                    "data": doc.data,
                    "media_type": doc.media_type,
                    "type": doc.type,
                },
                "title": doc.title,
                "type": "document",
            }
        )

    payload = {
        "model": "claude-opus-4-1-20250805",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": content,
            }
        ],
    }
    headers = {
        "x-api-key": f"{os.getenv('ANTHROPIC_API_KEY')}",
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }

    print("anth_cite params:")
    print(json.dumps(payload, indent=2))
    print("")

    async with httpx.AsyncClient() as client:
        response_dict = {}

        try:
            response = await client.post(url, json=payload, headers=headers, timeout=30)
            response_dict = response.json()
        except httpx.HTTPStatusError as e:
            print(f"http error: {e.response.status_code} - {e.response.text}")
            response_dict = {
                "error": e.response.text,
                "status_code": e.response.status_code,
            }
        except httpx.ReadTimeout as e:
            print(f"http read timeout - url '{e.request.url}', error '{e}'")
        except httpx.RequestError as e:
            print(f"http request error - url '{e.request.url}', error '{e}'")

    return response_dict
