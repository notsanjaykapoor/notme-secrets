import os

import anthropic
import httpx
import pydantic_ai

url = "https://api.parallel.ai/v1beta/search"


async def anth_search(
    context: pydantic_ai.RunContext[str],
    query: str,
    max_uses: int = 5,
) -> list[dict]:
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

    print("anth_search params:")
    print(payload)
    print("")

    async with anthropic.AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY")) as client:
        results_list = []

        try:
            response = await client.messages.create(**payload)

            breakpoint() #
            # response = await client.post(url, json=payload, headers=headers)
            # response_json = response.json()
            # results_list = response_json.get("results")
        except httpx.HTTPStatusError as e:
            print(f"http error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"http request error - url '{e.request.url}', error '{e}'")

    return results_list
