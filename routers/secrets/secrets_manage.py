import json
import secrets

import fastapi
import fastapi.responses
import fastapi.templating

import context
import log
import main_shared
import pydantic
import sqlmodel

import services.secrets
import services.crypto_keys.gpg

logger = log.init("app")

# initialize templates dir
templates = fastapi.templating.Jinja2Templates(directory="routers", context_processors=[main_shared.jinja_context])

app = fastapi.APIRouter(
    tags=["app"],
    dependencies=[fastapi.Depends(main_shared.get_db)],
    responses={404: {"description": "Not found"}},
)


class SecretNewStruct(pydantic.BaseModel):
    name: str
    password: str
    user: str | None


@app.post("/secrets/create", response_class=fastapi.responses.JSONResponse)
def secrets_create(
    request: fastapi.Request,
    secret_new_struct: SecretNewStruct,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
    db_session: sqlmodel.Session = fastapi.Depends(main_shared.get_db),
):
    logger.info(f"{context.rid_get()} secrets user {user_id} create '{secret_new_struct.name}' try")

    try:
        # get default user key
        user_key = services.crypto_keys.get_user_default(
            db_session=db_session,
            user_id=user_id,
        )

        # create cipher text from raw data
        data = {
            "passw": secret_new_struct.password,
            "user": secret_new_struct.user
        }
        pgp_msg = services.crypto_keys.gpg.encrypt(key=user_key, plain_text=json.dumps(data))

        # create database secret
        services.secrets.create(
            db_session,
            data_cipher=pgp_msg,
            key_id=user_key.id,
            name=secret_new_struct.name,
            user_id=user_id,
        )

        logger.info(f"{context.rid_get()} secrets user {user_id} create '{secret_new_struct.name}' ok")
    except Exception as e:
        logger.error(f"{context.rid_get()} secrets user {user_id} create '{secret_new_struct.name}' exception - {e}")

    response = fastapi.responses.JSONResponse(content={"response": "ok"})
    response.headers["HX-Redirect"] = "/secrets"

    return response


@app.get("/secrets/new", response_class=fastapi.responses.HTMLResponse)
def secrets_new(
    request: fastapi.Request,
    name: str,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
):
    logger.info(f"{context.rid_get()} secrets user {user_id} new")

    try:
        response = templates.TemplateResponse(
            request,
            "secrets/new.html",
            {
                "app_name": "Pass",
                "name": name,
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} secrets user {user_id} new render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    return response


@app.get("/secrets/new/generate", response_class=fastapi.responses.JSONResponse)
def secrets_new_generate(
    request: fastapi.Request,
    user_id: int = fastapi.Depends(main_shared.get_user_id),
):
    logger.info(f"{context.rid_get()} secrets user {user_id} generate")

    password = secrets.token_urlsafe(13)

    response = templates.TemplateResponse(
        request,
        "secrets/new_password.html",
        {
            "app_name": "Pass",
            "password": password,
        }
    )

    return response
