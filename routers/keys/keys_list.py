import fastapi
import fastapi.responses
import fastapi.templating
import sqlmodel

import context
import log
import main_shared
import services.crypto_keys
import services.secrets
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


@app.get("/keys", response_class=fastapi.responses.HTMLResponse)
def keys_list(
    request: fastapi.Request,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    query: str = "",
    offset: int = 0,
    limit: int = 50,
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    logger.info(f"{context.rid_get()} keys user {user.id} list")

    try:
        list_result = services.crypto_keys.list(
            db_session=db_session,
            query=query,
            offset=offset,
            limit=limit,
        )
        keys_list = list_result.objects
        keys_total = list_result.total

        # map each key to count of secrets
        keys_map = {key.id: services.secrets.count_by_key(db_session=db_session, key_id=key.id) for key in keys_list}

        query_code = 0
        query_result = f"query '{query}' returned {len(keys_list)} results"

        logger.info(f"{context.rid_get()} keys user {user.id} list ok - total {keys_total}")
    except Exception as e:
        keys_list = []
        keys_map = {}
        query_code = 500
        query_result = f"exception {e}"

        logger.error(f"{context.rid_get()} keys user {user.id} list exception '{e}'")

    if "HX-Request" in request.headers:
        template = "keys/list_table.html"
    else:
        template = "keys/list.html"

    try:
        response = templates.TemplateResponse(
            request,
            template,
            {
                "app_name": "Keys",
                "query": query,
                "query_code": query_code,
                "query_result": query_result,
                "keys_list": keys_list,
                "keys_map": keys_map,
                "user": user,
            },
        )

        if "HX-Request" in request.headers:
            response.headers["HX-Push-Url"] = f"/keys?query={query}"
    except Exception as e:
        logger.error(f"{context.rid_get()} keys user {user.id} list render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    return response
