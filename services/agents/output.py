import dataclasses
import json

import pydantic_ai
import pydantic_ai.messages
import pydantic_ai._agent_graph

import models


@dataclasses.dataclass
class OutputStruct:
    kind: str
    text: str


def output_model_msg(model_msg: pydantic_ai.messages.ModelMessage) -> OutputStruct:
    if model_msg.kind == "request":
        text = output_model_request(msg=model_msg)
    elif model_msg.kind == "response":
        text = output_model_response(msg=model_msg)

    return OutputStruct(
        kind=model_msg.kind,
        text=text,
    )


def output_node(node: pydantic_ai._agent_graph.AgentNode) -> OutputStruct:
    if pydantic_ai.Agent.is_user_prompt_node(node):
        # skip node
        kind = "user"
        text = ""
    elif pydantic_ai.Agent.is_model_request_node(node):
        kind = "request"
        text = output_model_request(msg=node.request)
    elif pydantic_ai.Agent.is_call_tools_node(node):
        kind = "response"
        text = output_model_response(msg=node.model_response)
    elif pydantic_ai.Agent.is_end_node(node):
        kind = "end"
        text = node.data.output
    else:
        # should not happen
        pass

    return OutputStruct(
        kind=kind,
        text=text,
    )


def output_model_request(msg: pydantic_ai.messages.ModelRequest) -> str:
    """
    Map model request to an output string.

    A model request can have parts with type:
        - SystemPromptPart
        - UserPromptPart
        - ToolReturnPart
        - RetryPromptPart

    docs: https://ai.pydantic.dev/api/messages/
    """
    output = []

    for part in msg.parts:
        if part.part_kind == "user-prompt":
            if len(output) == 0:
                output.append("user:")
            output.append(part.content)
        elif part.part_kind == "tool-return":
            if len(output) == 0:
                output.append("tool:")
            output.append(f"tool return '{part.tool_name}'")
        elif part.part_kind == "system-prompt":
            pass
        else:
            output.append(f"tool part '{part.part_kind}' todo")

    return " ".join(output)


def output_model_response(msg: pydantic_ai.messages.ModelResponse) -> str:
    """
    Map model response to an output string.

    A model response can have parts with type:
        - TextPart
        - ToolCallPart, BuiltinToolCallPart
        - ThinkingPart

    docs: https://ai.pydantic.dev/api/messages/
    """
    output = []

    for part in msg.parts:
        if part.part_kind == "text":
            output.append(part.content)
        elif part.part_kind == "thinking":
            output.append("thinking part todo")  # todo
        elif part.part_kind in ["builtin-tool-call", "tool-call"]:
            if len(output) == 0:
                if part.part_kind == "builtin-tool-call":
                    output.append("builtin-tool:")
                else:
                    output.append("tool:")
            output.append(f"tool call '{part.tool_name}'.")
        elif part.part_kind == "builtin-tool-return":
            pass
        else:
            output.append(f"tool part '{part.part_kind}' todo")

    return " ".join(output)


def output_tool(output: dict | str) -> str:
    """
    Map tool output to a properly formatted string.

    If output is a dict, format it as a markdown string based on its format.
    """
    if isinstance(output, str):
        return output

    if isinstance(output, dict):
        if "places" in output:
            return _output_places_markdown(places=output.get("places"))
        # default dict output
        return json.dumps(output)

    return ""


def _output_places_markdown(places: list[models.Place]) -> str:
    """
    Convert list of places to markdown text
    """
    md_list = []

    md_list.append(f"here are {len(places)} matching places:\n\n")

    for place in places:
        md_list.append(f"**{place.name}, {place.city}**\n")

        if place.brands_count > 0:
            md_list.append(f"- brands: {place.brands_string}\n")

        if place.website:
            md_list.append(f"- website: {place.website}\n")

        md_list.append("\n")

    return "".join(md_list)
