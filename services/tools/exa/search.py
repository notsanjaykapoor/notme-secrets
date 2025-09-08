import json
import os

import httpx
import pydantic_ai

url = "https://api.exa.ai/search"


async def exa_search(
    context: pydantic_ai.RunContext[str], query: str, contents: dict = {}, type: str = "auto", limit: int = 10
) -> list[dict]:
    """
    Search the web.

    Args:
      query: The query string for the search.
      limit: Number of results to return.

    Returns:
      A list of search results containing title, URL, published date, and author.

    Docs:
        - https://docs.exa.ai/reference/search
    """
    payload = {
        "contents": contents,
        "numResults": limit,  # 10 is default, 100 is max
        "query": query,  # max of 5000 chars
        "type": type,  # default is auto
    }

    headers = {
        "x-api-key": f"{os.getenv('EXA_API_KEY')}",
        "Content-Type": "application/json",
    }

    print("exa_search params:")
    print(json.dumps(payload, indent=2))
    print("")

    async with httpx.AsyncClient() as client:
        results_list = []

        try:
            response = await client.post(url, json=payload, headers=headers)
            response_json = response.json()
            results_list = response_json.get("results")
        except httpx.HTTPStatusError as e:
            print(f"http error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"http request error - url '{e.request.url}', error '{e}'")

    return results_list
