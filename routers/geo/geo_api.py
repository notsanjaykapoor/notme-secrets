import fastapi
import fastapi.responses
import fastapi.templating
import sqlmodel

import context
import log
import main_shared
import services.geo
import services.places
import services.users

logger = log.init("app")

# initialize templates dir
templates = fastapi.templating.Jinja2Templates(directory="routers", context_processors=[main_shared.jinja_context])

app = fastapi.APIRouter(
    tags=["app"],
    dependencies=[fastapi.Depends(main_shared.get_db)],
    responses={404: {"description": "Not found"}},
)


@app.get("/geo/api/box/{box_name}", response_class=fastapi.responses.HTMLResponse)
def geo_api_query(
    request: fastapi.Request,
    box_name: str = "",
    query: str = "",
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    logger.info(f"{context.rid_get()} api query '{query}' box '{box_name}' try")

    geo_list = []
    places_source_ids = {}

    query_code = 0
    query_result = ""

    try:
        box = services.geo.get_by_slug(db_session=db_session, slug=box_name)

        if query:
            query_code, geo_list = services.places.geo_search_by_name(city=box, name=query)
            query_result = f"query '{query}' returned {len(geo_list)} results"

            # get current places to cross reference vs additions list
            places_struct = services.places.list(
                db_session=db_session,
                query=f"user_id:{user_id} city:{box.name}",
                offset=0,
                limit=100,
            )
            places_list = places_struct.objects
            places_source_ids = {place.source_id: place.id for place in places_list}
    except Exception as e:
        query_code = 500
        query_result = str(e)

    referer_path = f"/geo/places/box/{box.slug}"

    if "HX-Request" in request.headers:
        template = "geo/api/list_table.html"
    else:
        template = "geo/api/list.html"

    try:
        response = templates.TemplateResponse(
            request,
            template,
            {
                "add_code": 0,
                "app_name": "Geo - Api",
                "box": box,
                "geo_list": geo_list,
                "places_source_ids": places_source_ids,
                "referer_path": referer_path,
                "request_path": request.url.path,
                "query": query,
                "query_code": query_code,
                "query_result": query_result,
                "user": user,
            },
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} api render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} api query '{query}' box '{box_name}' ok")

    return response
