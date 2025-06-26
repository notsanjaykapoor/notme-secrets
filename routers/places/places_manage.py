import fastapi
import fastapi.responses
import fastapi.templating
import sqlmodel

import context
import log
import main_shared
import models
import services.geo
import services.goog_places
import services.mapbox
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

        code, place_db = services.places.create(
            db_session=db_session,
            user=user,
            city=box,
            geo_json=geo_json,
            name=geo_json.get("properties", {}).get("name"),
        )

        place_id = place_db.id
        add_code = 201

        logger.info(f"{context.rid_get()} places add box '{box_name}' source '{source_name}' ok")
    except Exception as e:
        place_id = 0
        add_code = 500
        logger.error(f"{context.rid_get()} places add box '{box_name}' source '{source_name} exception - '{e}'")

    # shared template with geo_mapbox list

    response = templates.TemplateResponse(
        request,
        "geo/mapbox/list_add_fragment.html",
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
                "place": place_db,
                "places_brands_path": f"/places/{place_db.id}/brands",
                "places_notes_path": f"/places/{place_db.id}/notes",
                "places_tags_path": f"/places/{place_db.id}/tags",
                "places_website_path": f"/places/{place_db.id}/website",
                "referer_path": request.headers.get("referer") or "/geo",
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


@app.get("/places/{place_id}/brands/{edit_op}", response_class=fastapi.responses.HTMLResponse)
def places_update_brands(
    request: fastapi.Request,
    place_id: int,
    edit_op: str,
    names: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    logger.info(f"{context.rid_get()} places {place_id} brands '{edit_op}' '{names}' try")

    place_db = services.places.get_by_id(db_session=db_session, id=place_id)

    brands_mod = [s.lower().strip() for s in names.split(",")]

    if edit_op == "add":
        place_db.brands = sorted(list(set(place_db.brands) | set(brands_mod)))
    else:
        place_db.brands = sorted(list(set(place_db.brands) - set(brands_mod)))

    db_session.add(place_db)
    db_session.commit()

    try:
        response = templates.TemplateResponse(
            request,
            "places/edit_brands.html",
            {
                "place": place_db,
                "places_brands_path": f"/places/{place_db.id}/brands",
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} places edit render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} places {place_id} brands '{edit_op}' '{names}' ok")

    return response

@app.get("/places/{place_id}/notes/mod", response_class=fastapi.responses.JSONResponse)
def places_update_notes(
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


@app.get("/places/{place_id}/tags/{edit_op}", response_class=fastapi.responses.HTMLResponse)
def places_update_tags(
    request: fastapi.Request,
    place_id: int,
    edit_op: str,
    names: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    logger.info(f"{context.rid_get()} places {place_id} tags '{edit_op}' '{names}' try")

    place_db = services.places.get_by_id(db_session=db_session, id=place_id)

    tags_mod = [s.lower().strip() for s in names.split(",")]

    if edit_op == "add":
        place_db.tags = sorted(list(set(place_db.tags) | set(tags_mod)))
    else:
        place_db.tags = sorted(list(set(place_db.tags) - set(tags_mod)))

    db_session.add(place_db)
    db_session.commit()

    try:
        response = templates.TemplateResponse(
            request,
            "places/edit_tags.html",
            {
                "place": place_db,
                "places_tags_path": f"/places/{place_db.id}/tags",
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} places edit render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    logger.info(f"{context.rid_get()} places {place_id} tags '{edit_op}' '{names}' ok")

    return response

@app.get("/places/{place_id}/website/mod", response_class=fastapi.responses.JSONResponse)
def places_uri_notes(
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
