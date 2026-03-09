import fastapi
import fastapi.responses
import fastapi.templating
import sqlmodel

import context
import log
import main_shared
import services.convs.reqs
import services.users

PASSW_BLUR_COUNT = 2
PASSW_BLUR_SECS = 3

logger = log.init("app")

# initialize templates dir
templates = fastapi.templating.Jinja2Templates(directory="routers", context_processors=[main_shared.jinja_context])

app = fastapi.APIRouter(
    tags=["app"],
    dependencies=[fastapi.Depends(main_shared.get_db)],
    responses={404: {"description": "Not found"}},
)


@app.get("/convs/reqs", response_class=fastapi.responses.HTMLResponse)
def convs_reqs_list(
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
        return fastapi.responses.RedirectResponse("/keys")

    logger.info(f"{context.rid_get()} convs reqs list '{query}'")

    try:
        conv_reqs_struct = services.convs.reqs.list(
            db_session=db_session,
            query=query,
            offset=offset,
            limit=limit,
            sort="id-"
        )
        conv_reqs_list = conv_reqs_struct.objects
        conv_reqs_total = conv_reqs_struct.total

        query_code = 0
        query_result = f"query '{query}' returned {len(conv_reqs_list)} results"

        logger.info(f"{context.rid_get()} convs reqs list '{query}' total {conv_reqs_total} ok")
    except Exception as e:
        conv_reqs_list = []
        query_code = 500
        query_result = f"exception {e}"

        logger.error(f"{context.rid_get()} convs reqs list '{query}' exception '{e}'")

    if "HX-Request" in request.headers:
        template = "convs/reqs/list_table.html"
    else:
        template = "convs/reqs/list.html"

    try:
        response = templates.TemplateResponse(
            request,
            template,
            {
                "app_name": "Conv Reqs",
                "query": query,
                "query_code": query_code,
                "query_result": query_result,
                "conv_reqs_list": conv_reqs_list,
                "user": user,
            },
        )

        if "HX-Request" in request.headers:
            response.headers["HX-Push-Url"] = f"/convs?query={query}"
    except Exception as e:
        logger.error(f"{context.rid_get()} convs reqs list '{query}' render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    return response
