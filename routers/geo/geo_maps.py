import os

import fastapi
import fastapi.responses
import fastapi.templating
import shapely
import sqlmodel

import context
import log
import main_shared
import services.cities
import services.geo
import services.places
import services.regions
import services.users

logger = log.init("app")

# initialize templates dir
templates = fastapi.templating.Jinja2Templates(directory="routers", context_processors=[main_shared.jinja_context])

app = fastapi.APIRouter(
    tags=["app"],
    dependencies=[fastapi.Depends(main_shared.get_db)],
    responses={404: {"description": "Not found"}},
)


@app.get("/geo/maps", response_class=fastapi.responses.HTMLResponse)
def geo_maps(
    request: fastapi.Request,
    query: str = "",
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    logger.info(f"{context.rid_get()} geo maps try")

    try:
        cities_names_slugs = services.cities.get_all_names_slugs(db_session=db_session)
        cities_count = len(cities_names_slugs)

        regions_names_slugs = services.regions.get_all_names_slugs(db_session=db_session)
        regions_count = len(regions_names_slugs)
    except Exception as e:
        logger.error(f"{context.rid_get()} geo maps exception '{e}'")

    try:
        response = templates.TemplateResponse(
            request,
            "geo/maps/index.html",
            {
                "app_name": "Geo - Maps",
                "cities_count": cities_count,
                "cities_names_slugs": cities_names_slugs,
                "regions_names_slugs": regions_names_slugs,
                "regions_count": regions_count,
                "user": user,
            },
        )

        if "HX-Request" in request.headers:
            response.headers["HX-Push-Url"] = f"/geo/maps?query={query}"
    except Exception as e:
        logger.error(f"{context.rid_get()} geo maps render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} geo maps ok")

    return response


@app.get("/geo/maps/resolve", response_class=fastapi.responses.HTMLResponse)
def geo_maps_resolve(
    request: fastapi.Request,
    box_name: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    logger.info(f"{context.rid_get()} geo maps box '{box_name}' resolve try")

    box = services.geo.get_by_name(db_session=db_session, name=box_name)

    if box:
        redirect_path = f"/geo/maps/box/{box.slug}"
    else:
        # try to create city
        code, city_db = services.cities.create(db_session=db_session, name=box_name)
        if city_db:
            redirect_path = f"/geo/maps/box/{city_db.slug}"
        else:
            redirect_path = "/geo/maps"

    response = fastapi.responses.RedirectResponse(redirect_path, status_code=200)
    response.headers["HX-Redirect"] = redirect_path

    logger.info(f"{context.rid_get()} geo maps box '{box_name}' resolve ok")

    return response


@app.get("/geo/maps/box/{box_name}", response_class=fastapi.responses.HTMLResponse)
def geo_maps_box(
    request: fastapi.Request,
    box_name: str,
    query: str = "",
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    logger.info(f"{context.rid_get()} maps box '{box_name}' query '{query}' try")

    try:
        box = services.geo.get_by_slug(db_session=db_session, slug=box_name)
        geo_api_path = f"/geo/api/box/{box.slug}"
    except Exception as e:
        logger.error(f"{context.rid_get()} maps box '{box_name}' exception '{e}'")

    mapbox_token = os.getenv("MAPBOX_TOKEN")

    if "HX-Request" in request.headers:
        template = "geo/maps/box/show_map.html"
    else:
        template = "geo/maps/box/show.html"

    try:
        response = templates.TemplateResponse(
            request,
            template,
            {
                "app_name": "Geo - Map",
                "box": box,
                "geo_api_path": geo_api_path,
                "mapbox_token": mapbox_token,
                "request_path": request.url.path,
                "query": query,
                "user": user,
            },
        )

        if "HX-Request" in request.headers:
            response.headers["HX-Push-Url"] = f"{request.url.path}?query={query}"
    except Exception as e:
        logger.error(f"{context.rid_get()} maps box render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} maps box '{box_name}' query '{query}' ok")

    return response


@app.get("/geo/maps/box/{box_name}/tileset", response_class=fastapi.responses.JSONResponse)
def geo_maps_box_tileset(
    request: fastapi.Request,
    box_name: str,
    query: str = "",
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    logger.info(f"{context.rid_get()} maps box '{box_name}' query '{query}' tileset try")

    try:
        # normalize query
        if query and ":" not in query:
            query_norm = f"name:{query}".strip()
        else:
            query_norm = query

        box = services.geo.get_by_slug(db_session=db_session, slug=box_name)

        places_query = f"{query_norm} {box.type}:{box.name} user_id:{user_id}".strip()
        places_struct = services.places.list(
            db_session=db_session, query=places_query, offset=0, limit=50, sort="name+"
        )
        places_list = places_struct.objects
        places_count = len(places_list)
        places_total = places_struct.total

        # generate geo_json tiles collection from places list that's used by mapbox
        places_tileset = services.places.list_tiles(places=places_list)

        if places_count > 1:
            # generate bounding box from list of places
            places_points = [shapely.Point(place.lon_f, place.lat_f) for place in places_list]
            places_multi = shapely.MultiPoint(places_points)
            places_bbox = places_multi.bounds
        else:
            # use bounding box from city/region object
            # places_bbox = [box.lon_max, box.lat_min, box.lon_max, box.lat_max]

            # keep current bounding box
            places_bbox = []
    except Exception as e:
        logger.error(f"{context.rid_get()} maps box render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} maps box '{box_name}' query '{query}' tileset ok")

    response = fastapi.responses.JSONResponse(
        content={
            "bbox": places_bbox,
            "tileset": {
                "type": "FeatureCollection",
                "features": places_tileset,
            },
            "total": places_total,
        },
        status_code=200,
    )

    return response
