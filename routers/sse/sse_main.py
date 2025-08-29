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


@app.get("/sse", response_class=fastapi.responses.StreamingResponse)
async def see_root(
    request: fastapi.Request,
    query: str="",
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    # user = services.users.get_by_id(db_session=db_session, id=user_id)

    logger.info(f"{context.rid_get()} sse query '{query}' try")

    return fastapi.responses.StreamingResponse(
        services.anthropic.stream(query=query, tools=services.anthropic.tools.list_schemas()),
        media_type="text/event-stream",
    )