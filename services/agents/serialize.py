import pydantic_ai.messages


def serialize_model_msgs(model_msgs: list[pydantic_ai.messages.ModelMessage]) -> list[dict]:
    """
    Serialize pydantic model messages to python dicts.

    This is called when the pydantic to_jsonable_python function fails, e.g.
      - TypeError: 'MockValSer' object cannot be converted to 'SchemaSerializer'
    """
    # convert models to dicts
    model_dicts_list = [model_msg.__dict__ for model_msg in model_msgs]

    for model_obj in model_dicts_list:
        if "timestamp" in model_obj.keys():
            # convert timestamps to strings
            model_obj["timestamp"] = model_obj["timestamp"].isoformat()

        if "usage" in model_obj.keys():
            model_obj["usage"] = model_obj["usage"].__dict__

        # convert model parts to dicts
        parts_list = model_obj.get("parts") or []
        parts_dicts_list = []

        for part_obj in parts_list:
            if not isinstance(part_obj, dict):
                # map to dict
                part_obj = part_obj.__dict__

            part_kind = part_obj.get("part_kind")

            if "timestamp" in part_obj.keys():
                # convert timestamps to strings
                part_obj["timestamp"] = part_obj["timestamp"].isoformat()

            if part_kind == "builtin-tool-return":
                # map content blocks to dicts
                content = part_obj.get("content", [])
                if isinstance(content, list):
                    content_block_dicts = [block.__dict__ for block in content]
                    part_obj["content"] = content_block_dicts

            parts_dicts_list.append(part_obj)

        model_obj["parts"] = parts_dicts_list

    return model_dicts_list
