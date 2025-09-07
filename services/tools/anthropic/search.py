import os

import httpx
import pydantic_ai

url = "https://api.anthropic.com/v1/messages"


async def anth_search(
    context: pydantic_ai.RunContext[str],
    query: str,
    max_uses: int = 5,
) -> dict:
    """
    Search the web.

    Args:
      query: The query string for the search.
      max_uses: Optional limit the number of searches per request.

    Returns:
        A list of search results containing type, text, and citations.
    """
    payload = {
        "model": "claude-opus-4-1-20250805",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": query}],
        "tools": [{"type": "web_search_20250305", "name": "web_search", "max_uses": max_uses}],
    }
    headers = {
        "x-api-key": f"{os.getenv('ANTHROPIC_API_KEY')}",
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }

    print("anth_search params:")
    print(payload)
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
