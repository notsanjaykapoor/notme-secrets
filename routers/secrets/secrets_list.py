import fastapi
import fastapi.responses
import fastapi.templating
import sqlmodel

import context
import log
import main_shared
import services.secrets
import services.storage.gcs
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


@app.get("/secrets", response_class=fastapi.responses.HTMLResponse)
def orgs_list(
    request: fastapi.Request,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    try:
        bucket_name = services.storage.gcs.bucket_name()

        logger.info(f"{context.rid_get()} secrets orgs list bucket '{bucket_name}'")

        org_names = services.storage.gcs.bucket_folders(bucket_name=bucket_name)

        logger.info(f"{context.rid_get()} secrets orgs list bucket '{bucket_name}' ok - orgs count {len(org_names)}")
    except Exception as e:
        org_names = []
        logger.error(f"{context.rid_get()} secrets orgs list exception '{e}'")

    if len(org_names) == 1:
        org_name = org_names[0]
        logger.info(f"{context.rid_get()} secrets orgs list bucket '{bucket_name}' ok - redirect to org '{org_name}")
        return fastapi.responses.RedirectResponse(f"/secrets/orgs/{org_name}")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    try:
        response = templates.TemplateResponse(
            request,
            "secrets/orgs_list.html",
            {
                "app_name": "Orgs",
                "org_names": org_names,
                "user": user,
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} secrets list orgs render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    return response


@app.get("/secrets/orgs/{org}", response_class=fastapi.responses.HTMLResponse)
def secrets_list(
    request: fastapi.Request,
    org: str,
    query: str="",
    offset: int=0,
    limit: int=50,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    logger.info(f"{context.rid_get()} secrets org '{org}' query '{query}' try")

    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    try:
        list_result = services.secrets.list(
            org=org,
            query=query,
            offset=offset,
            limit=limit,
        )
        secrets_list = list_result.objects

        query_code = 0
        query_result = f"query '{query}' returned {len(secrets_list)} results"

        logger.info(f"{context.rid_get()} secrets org '{org}' query '{query}' ok")
    except Exception as e:
        secrets_list = []
        query_code = 500
        query_result = f"exception {e}"

        logger.error(f"{context.rid_get()} secrets org '{org}' query '{query}' exception '{e}'")

    if "HX-Request" in request.headers:
        template = "secrets/secrets_list_table.html"
    else:
        template = "secrets/secrets_list.html"

    try:
        response = templates.TemplateResponse(
            request,
            template,
            {
                "app_name": "Org Secrets",
                "org": org,
                "passw_blur_count": PASSW_BLUR_COUNT,
                "passw_blur_secs": PASSW_BLUR_SECS,
                "secrets_list": secrets_list,
                "prompt_text": "search",
                "query": query,
                "query_code": query_code,
                "query_result": query_result,
                "user": user,
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} secrets list render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    if "HX-Request" in request.headers:
        response.headers["HX-Push-Url"] = f"{request.get('path')}?query={query}"

    return response


@app.get("/secrets/orgs/{org}/{name}/blur", response_class=fastapi.responses.HTMLResponse)
def secrets_blur(
    request: fastapi.Request,
    org: str,
    name: str,
):
    logger.info(f"{context.rid_get()} secrets org '{org}' name '{name}' blur try")

    try:
        secret = services.secrets.get_by_name(org=org, name=name)
    except Exception as e:
        secret = None
        logger.error(f"{context.rid_get()} secrets blur exception '{e}'")

    try:
        response = templates.TemplateResponse(
            request,
            "secrets/secret_show.html",
            {
                "app_name": "Pass",
                "org": org,
                "secret": secret,
            }
        )

        logger.info(f"{context.rid_get()} secrets org '{org}' name '{name}' blur ok")
    except Exception as e:
        logger.error(f"{context.rid_get()} secrets blur render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})
    
    return response


@app.get("/secrets/orgs/{org}/{name}/decrypt", response_class=fastapi.responses.HTMLResponse)
def secrets_decrypt(
    request: fastapi.Request,
    org: str,
    name: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
):
    logger.info(f"{context.rid_get()} secrets org '{org}' name '{name}' decrypt try")

    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    try:
        secret = services.secrets.get_by_name(org=org, name=name)
        secret = services.secrets.decrypt(secret=secret)

        logger.info(f"{context.rid_get()} secrets org '{org}' name '{name}' decrypt ok")
    except Exception as e:
        secret = None
        logger.error(f"{context.rid_get()} secrets org '{org}' name '{name}' decrypt exception '{e}'")

    try:
        response = templates.TemplateResponse(
            request,
            "secrets/secret_show.html",
            {
                "app_name": "Pass",
                "org": org,
                "secret": secret
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} secrets decrypt render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})
    
    return response
