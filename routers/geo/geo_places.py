import fastapi
import fastapi.responses
import fastapi.templating
import sqlmodel

import context
import log
import main_shared
import services.geo
import services.places
import services.places.tags
import services.users

logger = log.init("app")

# initialize templates dir
templates = fastapi.templating.Jinja2Templates(directory="routers", context_processors=[main_shared.jinja_context])

app = fastapi.APIRouter(
    tags=["app"],
    dependencies=[fastapi.Depends(main_shared.get_db)],
    responses={404: {"description": "Not found"}},
)

@app.get("/geo/places", response_class=fastapi.responses.HTMLResponse)
@app.get("/geo/places/box/{box_name}", response_class=fastapi.responses.HTMLResponse)
def geo_places_list(
    request: fastapi.Request,
    box_name: str="",
    query: str="",
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    logger.info(f"{context.rid_get()} places list query '{query}' box '{box_name}' try")

    # normalize query
    if query and ":" not in query:
        query_norm = f"name:{query}".strip()
    else:
        query_norm = query

    box = None
    map_path = ""
    mapbox_path = ""
    query_prompt = "search places anywhere"

    cities_names_slugs = services.cities.get_all_names_slugs(db_session=db_session)
    cities_count = len(cities_names_slugs)

    if box_name:
        if box := services.geo.get_by_slug(db_session=db_session, slug=box_name):
            query_norm = f"{query_norm} {box.type}:{box.name}".strip()
            query_prompt = f"search places near {box.name}"
            map_path = f"/geo/maps/box/{box.slug}"
            mapbox_path = f"/geo/mapbox/box/{box.slug}"

    try:
        places_struct = services.places.list(db_session=db_session, query=query_norm, offset=0, limit=50, sort="name+")
        places_list = places_struct.objects
        places_total = places_struct.total

        tags_all_list = sorted(list(services.places.tags.list_all(db_session=db_session, city=box)))
        tags_cur_list = sorted(places_struct.tags)

        query_code = 0
        query_result = f"query '{query}' returned {len(places_list)} results"
    except Exception as e:
        places_list = []
        places_total = 0
        query_code = 500
        query_result = str(e)

        logger.error(f"{context.rid_get()} places list exception '{e}'")

    if "HX-Request" in request.headers:
        template = "geo/places/list_table.html"
    else:
        template = "geo/places/list.html"

    try:
        response = templates.TemplateResponse(
            request,
            template,
            {
                "app_name": "Geo - Places",
                "box": box,
                "cities_count": cities_count,
                "cities_names_slugs": cities_names_slugs,
                "map_path": map_path,
                "mapbox_path": mapbox_path,
                "places_list": places_list,
                "places_total": places_total,
                "request_path": request.url.path,
                "query": query,
                "query_code": query_code,
                "query_prompt": query_prompt,
                "query_result": query_result,
                "tags_cur_list": tags_cur_list,
                "tags_all_list": tags_all_list,
                "user": user,
            }
        )

        if "HX-Request" in request.headers:
            response.headers["HX-Push-Url"] = f"{request.url.path}?query={query}"
    except Exception as e:
        logger.error(f"{context.rid_get()} places list render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} places list query '{query}' box '{box_name}' ok")

    return response
