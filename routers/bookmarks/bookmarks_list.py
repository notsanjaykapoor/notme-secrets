import fastapi
import fastapi.responses
import fastapi.templating
import sqlmodel

import context
import log
import main_shared
import services.bookmarks
import services.bookmarks.categories
import services.bookmarks.tags
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


@app.get("/bookmarks", response_class=fastapi.responses.HTMLResponse)
def bookmarks_list(
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

    logger.info(f"{context.rid_get()} bookmarks list query '{query}' try")

    categories_all_list = sorted(
        list(services.bookmarks.categories.list_all(db_session=db_session))
    )

    try:
        list_result = services.bookmarks.list(
            db_session=db_session,
            query=query,
            offset=offset,
            limit=limit,
        )

        bookmarks_list = list_result.objects
        categories_cur_list = sorted(list_result.categories)
        categories_cur_str = ",".join(categories_cur_list)
        tags_cur_list = sorted(list_result.tags)

        if categories_cur_list:
            # filter tags by categories
            tags_all_list = sorted(
                services.bookmarks.tags.list_by_categories(
                    db_session=db_session, categories=categories_cur_list
                )
            )
        else:
            tags_all_list = []

        query_code = 0
        query_result = f"query '{query}' returned {len(bookmarks_list)} results"

        logger.info(
            f"{context.rid_get()} bookmarks list query '{query}' ok - {len(bookmarks_list)} results"
        )
    except Exception as e:
        bookmarks_list = []

        query_code = 500
        query_result = f"exception {e}"

        logger.error(
            f"{context.rid_get()} bookmarks list query '{query}' exception '{e}'"
        )

    if "HX-Request" in request.headers:
        template = "bookmarks/list_table.html"
    else:
        template = "bookmarks/list.html"

    try:
        response = templates.TemplateResponse(
            request,
            template,
            {
                "app_name": "Bookmarks",
                "bookmarks_list": bookmarks_list,
                "categories_cur_list": categories_cur_list,
                "categories_cur_str": categories_cur_str,
                "categories_all_list": categories_all_list,
                "query": query,
                "query_code": query_code,
                "query_result": query_result,
                "tags_cur_list": tags_cur_list,
                "tags_all_list": tags_all_list,
                "user": user,
            },
        )

        if "HX-Request" in request.headers:
            response.headers["HX-Push-Url"] = f"/bookmarks?query={query}"
    except Exception as e:
        logger.error(
            f"{context.rid_get()} bookmarks list query '{query}' render exception '{e}'"
        )
        return templates.TemplateResponse(request, "500.html", {})

    return response
