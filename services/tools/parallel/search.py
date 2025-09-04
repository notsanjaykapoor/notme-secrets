import os

import httpx
import pydantic_ai

url = "https://api.parallel.ai/v1beta/search"


async def par_search(
    context: pydantic_ai.RunContext[str],
    objective: str,
    search_queries: list[str] = [],
    limit: int = 10,
) -> list[dict]:
    """
    Search the web.

    Args:
      objective: Natural-language description of what the web research goal is.
      search_queries: Optional search queries to guide the search.

    Returns:
        A list of search results containing title, URL, and a list of excerpts.
    """
    payload = {
        "objective": objective,  # max of 5000 chars
        "search_queries": search_queries[0:5],  # max is 5
        "processor": "base",
        "max_results": limit,
        "max_chars_per_result": 1000,  # min is 100, max is 30000
    }

    headers = {
        "x-api-key": f"{os.getenv('PARALLEL_API_KEY')}",
        "Content-Type": "application/json",
    }

    print("par_search params:")
    print(payload)
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
