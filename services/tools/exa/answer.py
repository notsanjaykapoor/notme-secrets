import json
import os

import httpx
import pydantic_ai

url = "https://api.exa.ai/answer"


async def exa_answer(context: pydantic_ai.RunContext[str], query: str, text: bool = False) -> dict:
    """
    Get an LLM answer to a question informed by Exa search results.

    Args:
      query: The question or query to answer.
      text: If true, the response includes full text content in the search results

    Returns:
      The response includes both the generated answer and the sources used to create it.

    Docs:
        - https://docs.exa.ai/reference/answer
    """
    payload = {
        "query": query,
        "text": text,
    }

    headers = {
        "x-api-key": f"{os.getenv('EXA_API_KEY')}",
        "Content-Type": "application/json",
    }

    print("exa_answer params:")
    print(json.dumps(payload, indent=2))
    print("")

    async with httpx.AsyncClient() as client:
        result_dict = {}

        try:
            response = await client.post(url, json=payload, headers=headers)
            result_dict = response.json()
        except httpx.HTTPStatusError as e:
            print(f"http error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"http request error - url '{e.request.url}', error '{e}'")

    return result_dict
