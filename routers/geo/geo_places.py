import fastapi
import fastapi.responses
import fastapi.templating
import sqlmodel

import context
import log
import main_shared
import routers.utils
import services.cities
import services.geo
import services.places
import services.places.brands
import services.places.tags
import services.users

logger = log.init("app")

# initialize templates dir
templates = fastapi.templating.Jinja2Templates(
    directory="routers", context_processors=[main_shared.jinja_context]
)

app = fastapi.APIRouter(
    tags=["app"],
    dependencies=[fastapi.Depends(main_shared.get_db)],
    responses={404: {"description": "Not found"}},
)


@app.get("/geo/places", response_class=fastapi.responses.HTMLResponse)
@app.get("/geo/places/box/{box_name}", response_class=fastapi.responses.HTMLResponse)
def geo_places_list(
    request: fastapi.Request,
    box_name: str = "",
    query: str = "",
    offset: int = 0,
    limit: int = 20,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    # normalize query
    query_scope = ""
    query_scope_default = "name:"
    if query and ":" not in query:
        query_norm = f"{query_scope_default}{query}".strip()
    else:
        query_norm = query

    logger.info(
        f"{context.rid_get()} places list query '{query_norm}' box '{box_name}' try"
    )

    box = None
    geo_api_path = ""
    geo_map_path = ""

    query_code = 0
    query_prompt = "search places"

    cities_names_slugs = services.cities.get_all_names_slugs(db_session=db_session)
    cities_count = len(cities_names_slugs)

    if box_name:
        if box := services.geo.get_by_slug(db_session=db_session, slug=box_name):
            query_scope = f"{box.type}:{box.name}"
            query_prompt = f"search places near {box.name}"
            geo_map_path = f"/geo/maps/box/{box.slug}"
            geo_api_path = f"/geo/api/box/{box.slug}"

    try:
        places_struct = services.places.list(
            db_session=db_session,
            query=query_norm,
            scope=query_scope,
            offset=offset,
            limit=limit,
            sort="name+",
        )
        places_list = places_struct.objects
        places_count = len(places_list)
        places_total = places_struct.total

        brands_cur_list = sorted(places_struct.brands)

        tags_all_list = sorted(
            list(services.places.tags.list_all(db_session=db_session, box=box))
        )
        tags_cur_list = sorted(places_struct.tags)
        tags_cur_str = ",".join(tags_cur_list)

        if tags_cur_list:
            # filter brands by tags
            brands_all_list = sorted(
                services.places.brands.list_by_box_tags(
                    db_session=db_session, box=box, tags=tags_cur_list
                )
            )
        else:
            brands_all_list = []

        if box:
            query_result = f"query '{query_norm}' near '{box.name}'"
            if places_total <= limit:
                query_result = f"{query_result} returned {len(places_list)} results"
            else:
                query_result = f"{query_result} returned {offset + 1} - {offset + places_count} of {places_total} results"
        else:
            query_result = f"query '{query_norm}'"
            if places_total <= limit:
                query_result = f"{query_result} returned {len(places_list)} results"
            else:
                query_result = f"{query_result} returned {offset + 1} - {offset + places_count} of {places_total} results"
    except Exception as e:
        places_list = []
        places_total = 0
        query_code = 500
        query_result = str(e)

        logger.error(f"{context.rid_get()} places list exception '{e}'")

    page_prev, page_next = routers.utils.page_links(
        path=request.url.path,
        params=request.query_params,
        limit=limit,
        total=places_total,
    )

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
                "brands_all_list": brands_all_list,
                "brands_cur_list": brands_cur_list,
                "cities_count": cities_count,
                "cities_names_slugs": cities_names_slugs,
                "geo_api_path": geo_api_path,
                "geo_map_path": geo_map_path,
                "page_next": page_next,
                "page_prev": page_prev,
                "places_list": places_list,
                "places_total": places_total,
                "request_path": request.url.path,
                "query": query_norm,
                "query_code": query_code,
                "query_prompt": query_prompt,
                "query_result": query_result,
                "query_scope_default": query_scope_default,
                "tags_all_list": tags_all_list,
                "tags_cur_list": tags_cur_list,
                "tags_cur_str": tags_cur_str,
                "user": user,
            },
        )

        if "HX-Request" in request.headers:
            response.headers["HX-Push-Url"] = f"{request.url.path}?query={query}"
    except Exception as e:
        logger.error(f"{context.rid_get()} places list render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(
        f"{context.rid_get()} places list query '{query_norm}' box '{box_name}' ok"
    )

    return response
