import json

import fastapi
import fastapi.responses
import fastapi.templating
import sqlmodel

import context
import log
import main_shared
import models
import services.crypto_keys.gpg
import services.secrets
import services.secrets.fs
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
def secrets_list(
    request: fastapi.Request,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    query: str="",
    offset: int=0,
    limit: int=50,
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    user = services.users.get_by_id(db_session=db_session, id=user_id)

    logger.info(f"{context.rid_get()} secrets user {user.id} list")

    try:
        list_result = services.secrets.list(
            db_session=db_session,
            query=query,
            offset=offset,
            limit=limit,
            scope=f"user_id:{user_id}"
        )
        secrets_list = list_result.objects
        secrets_total = list_result.total

        # create map of secret id to secret data in plaintext format
        secrets_map = {secret.id : models.SecretData for secret in secrets_list}
        query_code = 0
        query_result = f"query '{query}' returned {len(secrets_list)} results"

        logger.info(f"{context.rid_get()} secrets user {user.id} list ok - total {secrets_total}")
    except Exception as e:
        secrets_list = []
        secrets_map = {}
        query_code = 500
        query_result = f"exception {e}"

        logger.error(f"{context.rid_get()} secrets user {user.id} list exception '{e}'")

    if "HX-Request" in request.headers:
        template = "secrets/list_table.html"
    else:
        template = "secrets/list.html"

    try:
        response = templates.TemplateResponse(
            request,
            template,
            {
                "app_name": "Secrets",
                "passw_blur_count": PASSW_BLUR_COUNT,
                "passw_blur_secs": PASSW_BLUR_SECS,
                "query": query,
                "query_code": query_code,
                "query_result": query_result,
                "secrets_list": secrets_list,
                "secrets_map": secrets_map,
                "user": user,
            }
        )

        if "HX-Request" in request.headers:
            response.headers["HX-Push-Url"] = f"/secrets?query={query}"
    except Exception as e:
        logger.error(f"{context.rid_get()} secrets user {user.id} list render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    return response


@app.get("/secrets/{secret_id}/blur", response_class=fastapi.responses.HTMLResponse)
def secrets_blur(
    request: fastapi.Request,
    secret_id: int,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    try:
        secret_db = services.secrets.get_by_id_user(
            db_session=db_session,
            id=secret_id,
            user_id=user_id,
        )
        logger.info(f"{context.rid_get()} secrets user '{user_id}' name '{secret_db.name}' blur ok")
    except Exception as e:
        secret_db = None
        logger.error(f"{context.rid_get()} secrets user '{user_id}' name '{secret_db.name}' blur exception '{e}'")

    secret_data = models.SecretData

    try:
        response = templates.TemplateResponse(
            request,
            "secrets/show.html",
            {
                "secret": secret_db,
                "secret_data": secret_data,
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} secrets blur render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})
    
    return response


@app.get("/secrets/{secret_id}/decrypt", response_class=fastapi.responses.HTMLResponse)
def secrets_decrypt(
    request: fastapi.Request,
    secret_id: int,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    if user_id == 0:
        return fastapi.responses.RedirectResponse("/login")

    try:
        secret_db = services.secrets.get_by_id_user(
            db_session=db_session,
            id=secret_id,
            user_id=user_id,
        )

        if not secret_db:
            raise "secret invalid"

        # get default user key
        user_key = services.crypto_keys.get_user_default(
            db_session=db_session,
            user_id=user_id,
        )

        logger.info(f"{context.rid_get()} secrets user '{user_id}' name '{secret_db.name}' decrypt try")

        plain_text = services.crypto_keys.gpg.decrypt(key=user_key, pgp_msg=secret_db.data_cipher)
        plain_dict = json.loads(plain_text)

        secret_data = models.SecretData(
            name=secret_db.name,
            passw=plain_dict.get("passw"),
            user=plain_dict.get("user")
        )

        logger.info(f"{context.rid_get()} secrets user '{user_id}' name '{secret_db.name}' decrypt ok")
    except Exception as e:
        secret_data = None
        logger.error(f"{context.rid_get()} secrets user '{user_id}' name '{secret_db.name}' decrypt exception '{e}'")

    try:
        response = templates.TemplateResponse(
            request,
            "secrets/show.html",
            {
                "secret": secret_db,
                "secret_data": secret_data,
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} secrets decrypt render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})
    
    return response
