import os

import anthropic

MAX_TOKENS_DEFAULT = 1024
MODEL_DEFAULT = "claude-sonnet-4-20250514"

async def stream(query: str, tools: list[dict]):
    """
    Query model using the streaming interface.

    Async generator function that yield stream text chunks
    """
    client = anthropic.Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        default_headers={},
    )

    try:
        with client.messages.stream(
            model=MODEL_DEFAULT,
            max_tokens=MAX_TOKENS_DEFAULT,
            messages=[
                {
                    "content": query,
                    "role": "user",
                }
            ],
            tool_choice={
                "type": "auto" # claude decides to use or not
            },
            tools=tools,
        ) as stream:
            for text in stream.text_stream:
                print(f"stream text: {text}")

                yield f"data: {text}\n\n"
    except Exception as e:
        yield f"stream exception: {e}"


