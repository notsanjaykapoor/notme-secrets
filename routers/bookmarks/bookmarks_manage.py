import fastapi
import fastapi.responses
import fastapi.templating
import pydantic
import sqlmodel

import context
import log
import main_shared
import models
import services.bookmarks
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


class BookmarkStruct(pydantic.BaseModel):
    categories: str
    name: str
    uri: str


@app.post("/bookmarks/create", response_class=fastapi.responses.JSONResponse)
def bookmarks_create(
    request: fastapi.Request,
    bm_struct: BookmarkStruct,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    logger.info(f"{context.rid_get()} bookmarks create '{bm_struct.name}' try")

    bm = services.bookmarks.create(
        db_session=db_session,
        categories=[s.lower().strip() for s in bm_struct.categories.split(",") if s],
        name=bm_struct.name,
        user_id=user.id,
        uri=bm_struct.uri,
    )

    logger.info(
        f"{context.rid_get()} bookmarks create '{bm_struct.name}' ok - id {bm.id}"
    )

    response = fastapi.responses.JSONResponse(content={"response": "ok"})
    response.headers["HX-Redirect"] = f"/bookmarks/{bm.id}/edit"

    return response


@app.get("/bookmarks/{bookmark_id}/edit", response_class=fastapi.responses.JSONResponse)
def bookmarks_edit(
    request: fastapi.Request,
    bookmark_id: int,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    bm = services.bookmarks.get_by_id(db_session=db_session, id=bookmark_id)

    logger.info(f"{context.rid_get()} bookmarks {bm.id} edit try")

    referer_path = request.headers.get("referer")

    if "new" in referer_path:
        referer_path = _bookmarks_post_create_path(bm=bm)

    try:
        response = templates.TemplateResponse(
            request,
            "bookmarks/edit.html",
            {
                "app_name": "Edit Bookmark",
                "bm": bm,
                "bm_categories_path": f"/bookmarks/{bm.id}/categories",
                "bm_links_path": f"/bookmarks/{bm.id}/links",
                "bm_name_path": f"/bookmarks/{bm.id}/name/mod",
                "bm_notes_path": f"/bookmarks/{bm.id}/notes/mod",
                "bm_tags_path": f"/bookmarks/{bm.id}/tags",
                "bm_uri_path": f"/bookmarks/{bm.id}/uri/mod",
                "referer_path": referer_path,
                "user": user,
            },
        )

        logger.info(f"{context.rid_get()} bookmarks {bm.id} edit ok")
    except Exception as e:
        logger.error(f"{context.rid_get()} bookmarks new render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    return response


@app.get(
    "/bookmarks/{bookmark_id}/categories/{edit_op}",
    response_class=fastapi.responses.JSONResponse,
)
def bookmarks_edit_categories(
    request: fastapi.Request,
    bookmark_id: int,
    edit_op: str,
    categories: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    try:
        bm = services.bookmarks.get_by_id(db_session=db_session, id=bookmark_id)

        logger.info(
            f"{context.rid_get()} bookmarks {bm.id} edit categories {edit_op} '{categories}' try"
        )

        categories_mod = [s.lower().strip() for s in categories.split(",")]

        if edit_op == "add":
            bm.categories = sorted(list(set(bm.categories) | set(categories_mod)))
        else:
            bm.categories = sorted(list(set(bm.categories) - set(categories_mod)))

        db_session.add(bm)
        db_session.commit()

        logger.info(
            f"{context.rid_get()} bookmarks {bm.id} edit categories {edit_op} '{categories}' ok"
        )
    except Exception as e:
        logger.error(
            f"{context.rid_get()} bookmarks {bm.id} edit categories exception '{e}'"
        )
        return templates.TemplateResponse(request, "500.html", {})

    try:
        response = templates.TemplateResponse(
            request,
            "bookmarks/edit_categories.html",
            {
                "bm": bm,
                "bm_categories_path": f"/bookmarks/{bm.id}/categories",
                "user": user,
            },
        )
    except Exception as e:
        logger.error(
            f"{context.rid_get()} bookmarks {bm.id} edit categories render exception '{e}'"
        )
        return templates.TemplateResponse(request, "500.html", {})

    return response


@app.get(
    "/bookmarks/{bookmark_id}/links/{edit_op}",
    response_class=fastapi.responses.JSONResponse,
)
def bookmarks_edit_links(
    request: fastapi.Request,
    bookmark_id: int,
    edit_op: str,
    link: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    try:
        bm = services.bookmarks.get_by_id(db_session=db_session, id=bookmark_id)

        logger.info(
            f"{context.rid_get()} bookmarks {bm.id} links {edit_op} '{link}' try"
        )

        if edit_op == "add":
            if not link.startswith("https://"):
                raise ValueError("link invalid")

            bm.links = bm.links + [link]
        else:
            bm.links = [s for s in bm.links if s != link]

        db_session.add(bm)
        db_session.commit()

        logger.info(
            f"{context.rid_get()} bookmarks {bm.id} links {edit_op} '{link}' ok"
        )
    except Exception as e:
        logger.error(
            f"{context.rid_get()} bookmarks {bm.id} links {edit_op} exception '{e}'"
        )

    try:
        response = templates.TemplateResponse(
            request,
            "bookmarks/edit_links.html",
            {
                "bm": bm,
                "bm_links_path": f"/bookmarks/{bm.id}/links",
                "user": user,
            },
        )
    except Exception as e:
        logger.error(
            f"{context.rid_get()} bookmarks {bm.id} links add render exception '{e}'"
        )
        return templates.TemplateResponse(request, "500.html", {})

    return response


@app.get(
    "/bookmarks/{bookmark_id}/name/mod", response_class=fastapi.responses.JSONResponse
)
def bookmarks_edit_name(
    request: fastapi.Request,
    bookmark_id: int,
    name: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    try:
        bm = services.bookmarks.get_by_id(db_session=db_session, id=bookmark_id)

        logger.info(f"{context.rid_get()} bookmarks {bm.id} edit name try")

        bm.name = name

        db_session.add(bm)
        db_session.commit()

        logger.info(f"{context.rid_get()} bookmarks {bm.id} edit name ok")
    except Exception as e:
        logger.error(f"{context.rid_get()} bookmarks {bm.id} edit name exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    try:
        response = templates.TemplateResponse(
            request,
            "bookmarks/edit_name.html",
            {
                "bm": bm,
                "bm_name_path": f"/bookmarks/{bm.id}/name/mod",
                "user": user,
            },
        )
    except Exception as e:
        logger.error(
            f"{context.rid_get()} bookmarks {bm.id} edit notes render exception '{e}'"
        )
        return templates.TemplateResponse(request, "500.html", {})

    return response


@app.get(
    "/bookmarks/{bookmark_id}/notes/mod", response_class=fastapi.responses.JSONResponse
)
def bookmarks_edit_notes(
    request: fastapi.Request,
    bookmark_id: int,
    notes: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    try:
        bm = services.bookmarks.get_by_id(db_session=db_session, id=bookmark_id)

        logger.info(f"{context.rid_get()} bookmarks {bm.id} edit notes try")

        bm.notes = notes

        db_session.add(bm)
        db_session.commit()

        logger.info(f"{context.rid_get()} bookmarks {bm.id} edit notes ok")
    except Exception as e:
        logger.error(
            f"{context.rid_get()} bookmarks {bm.id} edit notes exception '{e}'"
        )
        return templates.TemplateResponse(request, "500.html", {})

    try:
        response = templates.TemplateResponse(
            request,
            "bookmarks/edit_notes.html",
            {
                "bm": bm,
                "bm_notes_path": f"/bookmarks/{bm.id}/notes/mod",
                "user": user,
            },
        )
    except Exception as e:
        logger.error(
            f"{context.rid_get()} bookmarks {bm.id} edit notes render exception '{e}'"
        )
        return templates.TemplateResponse(request, "500.html", {})

    return response


@app.get(
    "/bookmarks/{bookmark_id}/tags/{edit_op}",
    response_class=fastapi.responses.JSONResponse,
)
def bookmarks_edit_tags(
    request: fastapi.Request,
    bookmark_id: int,
    edit_op: str,
    tags: str = "",
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    try:
        bm = services.bookmarks.get_by_id(db_session=db_session, id=bookmark_id)

        logger.info(
            f"{context.rid_get()} bookmarks {bm.id} edit tags {edit_op} '{tags}' try"
        )

        tags_mod = [tag.lower().strip() for tag in tags.split(",")]

        if edit_op == "add":
            bm.tags = sorted(list(set(bm.tags) | set(tags_mod)))
        else:
            bm.tags = sorted(list(set(bm.tags) - set(tags_mod)))

        db_session.add(bm)
        db_session.commit()

        logger.info(
            f"{context.rid_get()} bookmarks {bm.id} edit tags {edit_op} '{tags}' ok"
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} bookmarks {bm.id} edit tags exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    try:
        response = templates.TemplateResponse(
            request,
            "bookmarks/edit_tags.html",
            {
                "bm": bm,
                "bm_tags_path": f"/bookmarks/{bm.id}/tags",
                "user": user,
            },
        )
    except Exception as e:
        logger.error(
            f"{context.rid_get()} bookmarks {bm.id} edit tags render exception '{e}'"
        )
        return templates.TemplateResponse(request, "500.html", {})

    return response


@app.get(
    "/bookmarks/{bookmark_id}/uri/mod", response_class=fastapi.responses.JSONResponse
)
def bookmarks_edit_uri(
    request: fastapi.Request,
    bookmark_id: int,
    uri: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    try:
        bm = services.bookmarks.get_by_id(db_session=db_session, id=bookmark_id)

        logger.info(f"{context.rid_get()} bookmarks {bm.id} edit uri try")

        bm.uri = uri

        db_session.add(bm)
        db_session.commit()

        logger.info(f"{context.rid_get()} bookmarks {bm.id} edit uri ok")
    except Exception as e:
        logger.error(f"{context.rid_get()} bookmarks {bm.id} edit uri exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    try:
        response = templates.TemplateResponse(
            request,
            "bookmarks/edit_uri.html",
            {
                "bm": bm,
                "bm_uri_path": f"/bookmarks/{bm.id}/uri/mod",
                "user": user,
            },
        )
    except Exception as e:
        logger.error(
            f"{context.rid_get()} bookmarks {bm.id} edit uri render exception '{e}'"
        )
        return templates.TemplateResponse(request, "500.html", {})

    return response


@app.get("/bookmarks/new", response_class=fastapi.responses.HTMLResponse)
def bookmarks_new(
    request: fastapi.Request,
    name: str = "",
    cats: str = "",
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    logger.info(f"{context.rid_get()} bookmarks new '{name}' try")

    try:
        response = templates.TemplateResponse(
            request,
            "bookmarks/new.html",
            {
                "app_name": "New Bookmark",
                "cats_str": cats,
                "name": name,
                "user": user,
            },
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} bookmarks new render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    return response


def _bookmarks_post_create_path(bm: models.Bookmark) -> str:
    """
    Generate bookmarks path to redirect to after creating a new bookmark.
    """
    if bm.categories:
        cats_str = ",".join(bm.categories)
        return f"/bookmarks?query=cats:{cats_str}"

    return "/bookmarks"
