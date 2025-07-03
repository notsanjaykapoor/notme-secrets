import fastapi
import fastapi.responses
import fastapi.templating
import sqlmodel

import context
import log
import main_shared
import models
import services.cities
import services.geo
import services.goog_places
import services.mapbox
import services.places
import services.places.brands
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

@app.get("/places/add", response_class=fastapi.responses.HTMLResponse)
def places_add(
    request: fastapi.Request,
    box_name: str,
    source_id: str,
    source_name: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    logger.info(f"{context.rid_get()} places add box '{box_name}' source '{source_name}' try")

    try:
        box = services.geo.get_by_slug(db_session=db_session, slug=box_name)

        if source_name == models.place.SOURCE_GOOGLE:
            geo_json = services.goog_places.get_by_id(goog_id=source_id)
        elif source_name == models.place.SOURCE_MAPBOX:
            geo_json = services.mapbox.get_by_id(mapbox_id=source_id)
        else:
            raise ValueError(f"invalid source {source_name}")

        if box.type != models.box.TYPE_CITY:
            # get or create city
            city_name = geo_json.get("properties", {}).get("city", "")
            country_code = geo_json.get("properties", {}).get("country", "")
            city = services.cities.get_by_name(db_session=db_session, name=city_name, country_code=country_code)

            if not city:
                _, city = services.cities.create(db_session=db_session, name=city_name, country_code=country_code)
        else:
            city = box

        code, place_db = services.places.create(
            db_session=db_session,
            user=user,
            city=city,
            geo_json=geo_json,
            name=geo_json.get("properties", {}).get("name"),
        )

        place_id = place_db.id
        add_code = code

        logger.info(f"{context.rid_get()} places add box '{box_name}' source '{source_name}' ok")
    except Exception as e:
        place_id = -1
        add_code = 500
        logger.error(f"{context.rid_get()} places add box '{box_name}' source '{source_name} exception - '{e}'")

    # shared template with geo_mapbox list

    response = templates.TemplateResponse(
        request,
        "geo/api/list_add_fragment.html",
        {
            "add_code": add_code,
            "box": box,
            "place_id": place_id,
            "source_id": source_id,
            "source_name": source_name,
        }
    )

    return response

@app.get("/places/{place_id}/edit", response_class=fastapi.responses.HTMLResponse)
def places_edit(
    request: fastapi.Request,
    place_id: int,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    logger.info(f"{context.rid_get()} places {place_id} edit try")

    place_db = services.places.get_by_id(db_session=db_session, id=place_id)

    brands_match_list = sorted(list(services.places.brands.list_all(db_session=db_session)))
    brands_match_list = sorted(set(brands_match_list) - set(place_db.brands))

    tags_match_list = sorted(list(services.places.tags.list_all(db_session=db_session, city=None)))
    tags_match_list = sorted(set(tags_match_list) - set(place_db.tags))

    if "HX-Request" in request.headers:
        template = ""
    else:
        template = "places/edit.html"

    try:
        response = templates.TemplateResponse(
            request,
            template,
            {
                "app_name": "Edit Place",
                "brand_add_link": f"/places/{place_db.id}/brands/add",
                "brands_match_list": brands_match_list,
                "place": place_db,
                "places_brands_path": f"/places/{place_db.id}/brands",
                "places_notes_path": f"/places/{place_db.id}/notes",
                "places_tags_path": f"/places/{place_db.id}/tags",
                "places_website_path": f"/places/{place_db.id}/website",
                "referer_path": request.headers.get("referer") or "/geo",
                "tag_add_link": f"/places/{place_db.id}/tags/add",
                "tags_match_list": tags_match_list,
                "user": user,
            }
        )

        if "HX-Request" in request.headers:
            response.headers["HX-Push-Url"] = f"{request.url.path}?query={query}"
    except Exception as e:
        logger.error(f"{context.rid_get()} places edit render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} places {place_id} edit ok")

    return response


@app.get("/places/{place_id}/brands/search", response_class=fastapi.responses.HTMLResponse)
def places_brands_search(
    request: fastapi.Request,
    place_id: int,
    name: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    logger.info(f"{context.rid_get()} places {place_id} brands 'search' '{name}' try")

    place_db = services.places.get_by_id(db_session=db_session, id=place_id)

    brand_search = name

    brands_all_list = sorted(list(services.places.brands.list_all(db_session=db_session)))

    if not name:
        brands_match_list = brands_all_list
    else:
        # filter brands by name
        brands_match_list = [tag for tag in brands_all_list if name in tag]

    brands_match_list = sorted(set(brands_match_list) - set(place_db.brands))

    try:
        response = templates.TemplateResponse(
            request,
            "places/search_brands_result.html",
            {
                "place": place_db,
                "brand_add_link": f"/places/{place_db.id}/brands/add",
                "brand_search": brand_search,
                "brands_match_list": brands_match_list,
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} places {place_id} brands 'search' exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} places {place_id} brands 'search' '{name}' ok")

    return response


@app.get("/places/{place_id}/brands/{edit_op}", response_class=fastapi.responses.HTMLResponse)
def places_brands_update(
    request: fastapi.Request,
    place_id: int,
    edit_op: str,
    value: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    logger.info(f"{context.rid_get()} places {place_id} brands '{edit_op}' '{value}' try")

    place_db = services.places.get_by_id(db_session=db_session, id=place_id)

    brands_mod = [s.lower().strip() for s in value.split(",")]

    if edit_op == "add":
        place_db.brands = sorted(list(set(place_db.brands) | set(brands_mod)))
    else:
        place_db.brands = sorted(list(set(place_db.brands) - set(brands_mod)))

    db_session.add(place_db)
    db_session.commit()

    brands_match_list = sorted(list(services.places.brands.list_all(db_session=db_session)))
    brands_match_list = sorted(set(brands_match_list) - set(place_db.brands))

    try:
        response = templates.TemplateResponse(
            request,
            "places/edit_brands.html",
            {   
                "brand_add_link": f"/places/{place_db.id}/brands/add",
                "brands_match_list": brands_match_list,
                "place": place_db,
                "places_brands_path": f"/places/{place_db.id}/brands",
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} places edit render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} places {place_id} brands '{edit_op}' '{value}' ok")

    return response


@app.get("/places/{place_id}/notes/mod", response_class=fastapi.responses.JSONResponse)
def places_notes_update(
    request: fastapi.Request,
    place_id: int,
    val: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    logger.info(f"{context.rid_get()} places {place_id} edit notes try")

    place_db = services.places.get_by_id(db_session=db_session, id=place_id)

    place_db.notes = val

    db_session.add(place_db)
    db_session.commit()

    try:
        response = templates.TemplateResponse(
            request,
            "places/edit_notes.html",
            {
                "place": place_db,
                "places_notes_path": f"/places/{place_db.id}/notes",
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} places edit render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} places {place_id} edit notes ok")

    return response


@app.get("/places/{place_id}/tags/search", response_class=fastapi.responses.HTMLResponse)
def places_tags_search(
    request: fastapi.Request,
    place_id: int,
    name: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    logger.info(f"{context.rid_get()} places {place_id} tags 'search' '{name}' try")

    place_db = services.places.get_by_id(db_session=db_session, id=place_id)

    tag_search = name

    tags_all_list = sorted(list(services.places.tags.list_all(db_session=db_session, city=None)))

    if not name:
        tags_match_list = tags_all_list
    else:
        # filter tags by name
        tags_match_list = [tag for tag in tags_all_list if name in tag]

    tags_match_list = sorted(set(tags_match_list) - set(place_db.tags))

    try:
        response = templates.TemplateResponse(
            request,
            "places/search_tags_result.html",
            {
                "place": place_db,
                "tag_add_link": f"/places/{place_db.id}/tags/add",
                "tag_search": tag_search,
                "tags_match_list": tags_match_list,
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} places {place_id} tags 'search' exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} places {place_id} tags 'search' '{name}' ok")

    return response


@app.get("/places/{place_id}/tags/{edit_op}", response_class=fastapi.responses.HTMLResponse)
def places_tags_update(
    request: fastapi.Request,
    place_id: int,
    edit_op: str,
    value: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    logger.info(f"{context.rid_get()} places {place_id} tags '{edit_op}' '{value}' try")

    place_db = services.places.get_by_id(db_session=db_session, id=place_id)

    tags_mod = [s.lower().strip() for s in value.split(",")]

    if edit_op == "add":
        place_db.tags = sorted(list(set(place_db.tags) | set(tags_mod)))
    else:
        place_db.tags = sorted(list(set(place_db.tags) - set(tags_mod)))

    db_session.add(place_db)
    db_session.commit()

    tags_match_list = sorted(list(services.places.tags.list_all(db_session=db_session, city=None)))
    tags_match_list = sorted(set(tags_match_list) - set(place_db.tags))

    try:
        response = templates.TemplateResponse(
            request,
            "places/edit_tags.html",
            {
                "place": place_db,
                "places_tags_path": f"/places/{place_db.id}/tags",
                "tag_add_link": f"/places/{place_db.id}/tags/add",
                "tags_match_list": tags_match_list,
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} places edit render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} places {place_id} tags '{edit_op}' '{value}' ok")

    return response

@app.get("/places/{place_id}/website/mod", response_class=fastapi.responses.JSONResponse)
def places_website_update(
    request: fastapi.Request,
    place_id: int,
    val: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    logger.info(f"{context.rid_get()} places {place_id} edit website try")

    place_db = services.places.get_by_id(db_session=db_session, id=place_id)

    if val == "" or val.startswith("https:"):
        place_db.website = val

        db_session.add(place_db)
        db_session.commit()

    try:
        response = templates.TemplateResponse(
            request,
            "places/edit_website.html",
            {
                "place": place_db,
                "places_website_path": f"/places/{place_db.id}/website",
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} places edit render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} places {place_id} edit website ok")

    return response
