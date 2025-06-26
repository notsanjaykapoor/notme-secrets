import time

import fastapi
import fastapi.responses
import fastapi.templating
import sqlmodel

import context
import log
import main_shared
import services.anthropic
import services.anthropic.tools
import services.users

logger = log.init("app")

# initialize templates dir
templates = fastapi.templating.Jinja2Templates(directory="routers", context_processors=[main_shared.jinja_context])

app = fastapi.APIRouter(
    tags=["app"],
    dependencies=[fastapi.Depends(main_shared.get_db)],
    responses={404: {"description": "Not found"}},
)


@app.get("/geo", response_class=fastapi.responses.HTMLResponse)
def geo_root(
    request: fastapi.Request,
    query: str="",
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    logger.info(f"{context.rid_get()} geo root query '{query}' try")

    query_code = 0
    query_error = ""
    query_ok = ""
    query_response = ""
    query_tools = ""

    try:
        if query:
            t_start = time.time()
            anthropic_message, antropic_struct = services.anthropic.query_tools(query=query, tools=services.anthropic.tools.list())
            t_secs = round(time.time() - t_start, 2)

            print("anthropic result")
            print(anthropic_message) # xxx

            query_response = ", ".join(antropic_struct.blocks_text)
            query_tools = ", ".join([tool_block.name for tool_block in antropic_struct.blocks_tools])
            query_ok = f"anthropic query completed in {t_secs}s"
    except Exception as e:
        query_code = 500
        query_response = f"exception {e}"

        logger.error(f"{context.rid_get()} geo root query '{query}' exception '{e}'")

    if "HX-Request" in request.headers:
        template = "geo/geo_query_result.html"
    else:
        template = "geo/geo_query.html"

    try:
        response = templates.TemplateResponse(
            request,
            template,
            {
                "app_name": "Geo",
                "query": query,
                "query_code": query_code,
                "query_error": query_error,
                "query_ok": query_ok,
                "query_prompt": "semantic query",
                "query_response": query_response,
                "query_tools": query_tools,
                "user": user,
            }
        )

        if "HX-Request" in request.headers:
            response.headers["HX-Push-Url"] = f"/geo?query={query}"
    except Exception as e:
        logger.error(f"{context.rid_get()} geo roo query '{query}' render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    return response
