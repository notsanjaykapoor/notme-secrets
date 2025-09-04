import sqlmodel

import models


def create(
    db_session: sqlmodel.Session, conv_id: int, data: dict, user_id: int, tags: list[str] = []
) -> tuple[int, models.ConvMsg]:
    """
    Create conversation database object.
    """
    parts_list = data.get("parts") or []

    if not parts_list:
        return 422, None

    parts_names = []
    tools_map = {}

    for part_obj in parts_list:
        part_kind = part_obj.get("part_kind")

        if part_kind in ["tool-call", "tool-return"]:
            tools_map[part_obj.get("tool_call_id")] = part_obj.get("tool_name")

        parts_names.append(part_kind)

    conv_msg_db = models.ConvMsg(
        conv_id=conv_id,
        data=data,
        kind=data.get("kind"),
        model_name=data.get("model_name") or "",
        parts_count=len(parts_names),
        parts_names=parts_names,
        provider_name=data.get("provider_name") or "",
        provider_response_id=data.get("provider_response_id") or "",
        tags=sorted(tags),
        tools_map=tools_map,
        usage=data.get("usage") or {},
        user_id=user_id,
    )

    db_session.add(conv_msg_db)
    db_session.commit()

    return 0, conv_msg_db
