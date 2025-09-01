import os

import anthropic

MAX_TOKENS_DEFAULT = 1024
MODEL_DEFAULT = "claude-sonnet-4-20250514"


async def stream(query: str, tools: list[dict]):
    """
    Query model using the streaming interface.

    Async generator function that yields stream text chunks
    """
    client = anthropic.Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        default_headers={},
    )

    try:
        params = {
            "max_tokens": MAX_TOKENS_DEFAULT,
            "messages": [
                {
                    "content": query,
                    "role": "user",
                }
            ],
            "model": MODEL_DEFAULT,
        }

        if tools:
            params["tool_choice"] = {"type": "auto"}
            params["tools"] = tools

        with client.messages.stream(**params) as stream:
            for text in stream.text_stream:
                print(f"stream text: {text}")

                yield f"data: {text}\n\n"
    except anthropic.APIStatusError as e:
        yield f"stream api status error {e.status_code}: {e}"
    except Exception as e:
        yield f"stream exception: {e}"
