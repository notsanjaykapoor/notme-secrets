import json

import pydantic_ai.messages

import models


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

    return " ".join(output)


def output_model_response(msg: pydantic_ai.messages.ModelResponse) -> str:
    """
    Map model response to an output string.

    A model response can have parts with type:
        - TextPart
        - ToolCallPart
        - ThinkingPart

    docs: https://ai.pydantic.dev/api/messages/
    """
    output = []

    for part in msg.parts:
        if part.part_kind == "text":
            output.append(part.content)
        elif part.part_kind == "thinking":
            output.append("thinking todo")  # todo
        elif part.part_kind == "tool-call":
            if len(output) == 0:
                output.append("tool:")
            output.append(f"tool call '{part.tool_name}'.")

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
