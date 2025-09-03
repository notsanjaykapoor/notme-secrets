import json
import os

import httpx

url = "https://api.parallel.ai/v1beta/search"


async def parallel_search(objective: str, search_queries: list[str] = []) -> str:
    """
    Search the web.

    Args:
      objective: Natural-language description of what the web research goal is. Include any source or freshness guidance.
      search_queries: Optional search queries to guide the search.

    Returns:
        list of places as a markdown string
    """
    payload = {
        "objective": objective,  # max of 5000 chars
        "search_queries": search_queries[0:5],  # max is 5
        "processor": "base",
        "max_results": 10,
        "max_chars_per_result": 1000,  # min is 100, max is 30000
    }

    headers = {
        "x-api-key": f"{os.getenv('PARALLEL_API_KEY')}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        results_list = []

        try:
            response = await client.post(url, json=payload, headers=headers)
            response_json = response.json()
            results_list = response_json.get("results")
        except httpx.HTTPStatusError as e:
            print(f"http error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"request error on {e.request.url}: {e}")

    return json.dumps(results_list)
