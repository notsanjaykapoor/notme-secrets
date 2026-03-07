import typing

import fastapi
import fastapi.responses
import fastapi.templating
import sqlmodel

import context
import log
import main_shared
import services.convs.msgs
import services.users

logger = log.init("app")

# initialize templates dir
templates = fastapi.templating.Jinja2Templates(directory="routers", context_processors=[main_shared.jinja_context])

app = fastapi.APIRouter(
    tags=["app"],
    dependencies=[fastapi.Depends(main_shared.get_db)],
    responses={404: {"description": "Not found"}},
)

@app.get("/convs/msgs", response_class=fastapi.responses.HTMLResponse)
def convs_mgs_list(
    request: fastapi.Request,
    query: str = "",
    offset: int = 0,
    limit: int = 50,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    if not user:
        return fastapi.responses.RedirectResponse("/convs")

    logger.info(f"{context.rid_get()} convs msgs query '{query}'")

    try:
        # if query:
        #     msgs_query = f"{msgs_query} {query}"

        msgs_struct = services.convs.msgs.list(db_session=db_session, query=query, offset=0, limit=1024, sort="id-")
        msgs_list = msgs_struct.objects
        msgs_total = msgs_struct.total

        query_code = 0
        query_result = f"query '{query}' returned {len(msgs_list)} results"

        logger.info(f"{context.rid_get()} convs msgs list '{query}' total {msgs_total} ok")

        # msgs_blocks = []

        # _code, model_msgs = services.convs.msgs.load_msgs(msgs_list=msgs_list)

        # for model_msg in model_msgs:
        #     output_struct = services.agents.output_model_msg(model_msg=model_msg)
        #     output_nodes = output_struct.nodes
        #     node_index = 0

        #     msg_block: dict[str, typing.Any] = {
        #         "role": "",
        #         "text": [],
        #     }

        #     while node_index < len(output_nodes):
        #         output_node = output_nodes[node_index]

        #         if output_node.name in ["user-prompt"]:
        #             if not msg_block.get("role"):
        #                 msg_block["role"] = "user"

        #             msg_block["text"].append(output_node.text)
        #             # services.console.print_fragment_user(f"user: {output_node.text}", end="\n\n")
        #         elif output_node.name in ["builtin-tool-call", "builtin-tool-return", "tool-call", "tool-return"]:
        #             if not msg_block.get("role"):
        #                 msg_block["role"] = "agent"

        #             msg_block["text"].append(output_node.text)
        #         elif output_node.name in ["model-text"]:
        #             if not msg_block.get("role"):
        #                 msg_block["role"] = "agent"

        #             # collect model-text nodes
        #             node_index, text = services.agents.output_nodes_collect(
        #                 output_nodes=output_nodes, name="model-text", index=node_index
        #             )
        #             msg_block["text"].append(text)
        #         elif output_node.name in ["model-end"]:
        #             # todo
        #             pass

        #         node_index += 1

        #     msg_block["text"] = "".join(msg_block["text"])
        #     msgs_blocks.append(msg_block)
    except Exception as e:
        msgs_list = []
        query_code = 500
        query_result = f"exception {e}"
        logger.error(f"{context.rid_get()} convs msgs list exception '{e}'")

    if "HX-Request" in request.headers:
        template = "convs/msgs/list_table.html"
    else:
        template = "convs/msgs/list.html"

    try:
        response = templates.TemplateResponse(
            request,
            template,
            {
                "app_name": "Conv Msgs",
                "query": query,
                "query_code": query_code,
                "query_result": query_result,
                "msgs_list": msgs_list,
                "user": user,
            },
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} convs msgs list render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    return response
