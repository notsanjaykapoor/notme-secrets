import dataclasses
import os

import anthropic
import anthropic.types.message

MAX_TOKENS_DEFAULT = 1024
MODEL_DEFAULT = "claude-sonnet-4-20250514"


@dataclasses.dataclass
class AnthropicMsgStruct:
    blocks_text: list[str]
    blocks_tools: list[list[dict]]
    blocks_total: int
    msg_role: str
    msg_stop: str


def query_doc(
    file_id: str, query: str
) -> tuple[anthropic.types.message.Message, AnthropicMsgStruct]:
    """
    Query model with a referenced document.

    The referenced document is file_id of a document that has already been uploaded to anthropic file storage.

    docs: https://docs.anthropic.com/en/docs/build-with-claude/files
    """
    client = anthropic.Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        default_headers={
            "anthropic-beta": "files-api-2025-04-14",  # required header for file api
        },
    )

    response = client.messages.create(
        model=MODEL_DEFAULT,
        max_tokens=MAX_TOKENS_DEFAULT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Answer the following question using the referenced document: {query}",
                    },
                    {
                        "type": "document",
                        "source": {
                            "type": "file",
                            "file_id": file_id,
                        },
                    },
                ],
            }
        ],
    )

    return response, _anthropic_message_parse(msg=response)


def query_tools(
    query: str, tools: list[dict]
) -> tuple[anthropic.types.message.Message, AnthropicMsgStruct]:
    """
    Query model with a set of tools that can be used.

    docs: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview
    """
    client = anthropic.Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        default_headers={},
    )

    response = client.messages.create(
        model=MODEL_DEFAULT,
        max_tokens=MAX_TOKENS_DEFAULT,
        messages=[
            {
                "content": query,
                "role": "user",
            }
        ],
        tool_choice={
            "type": "auto"  # claude decides to use or not
        },
        tools=tools,
    )

    return response, _anthropic_message_parse(msg=response)


def _anthropic_message_parse(
    msg: anthropic.types.message.Message,
) -> AnthropicMsgStruct:
    struct = AnthropicMsgStruct(
        blocks_text=[],
        blocks_tools=[],
        blocks_total=0,
        msg_role=msg.role,
        msg_stop=msg.stop_reason,
    )

    for block in msg.content:
        if isinstance(block, anthropic.types.TextBlock):
            struct.blocks_text.append(block.text)
            struct.blocks_total += 1
        elif isinstance(block, anthropic.types.ToolUseBlock):
            struct.blocks_tools.append(block)
            struct.blocks_total += 1

    return struct
