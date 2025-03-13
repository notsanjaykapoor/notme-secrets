import os
import secrets

import fastapi
import fastapi.responses
import fastapi.templating

import context
import log
import main_shared
import pydantic

import services.secrets

logger = log.init("app")

# initialize templates dir
templates = fastapi.templating.Jinja2Templates(directory="routers", context_processors=[main_shared.jinja_context])

app = fastapi.APIRouter(
    tags=["app"],
    dependencies=[fastapi.Depends(main_shared.get_db)],
    responses={404: {"description": "Not found"}},
)


class SecretStruct(pydantic.BaseModel):
    name: str
    password: str
    user: str | None


@app.get("/secrets/orgs/{org}/new", response_class=fastapi.responses.HTMLResponse)
def secrets_org_new(
    request: fastapi.Request,
    org: str,
):
    logger.info(f"{context.rid_get()} secrets org '{org}' new")

    try:
        response = templates.TemplateResponse(
            request,
            "secrets/new.html",
            {
                "app_name": "Pass",
                "org": org,
            }
        )
    except Exception as e:
        logger.error(f"{context.rid_get()} secrets org '{org}' new render exception '{e}'")
        return templates.TemplateResponse(request, "500.html", {})

    return response


@app.post("/secrets/orgs/{org}/create", response_class=fastapi.responses.JSONResponse)
def secrets_org_create(
    request: fastapi.Request,
    secret_struct: SecretStruct,
    org: str,
):
    logger.info(f"{context.rid_get()} secrets org '{org}' create '{secret_struct.name}'")

    crypt_struct = services.secrets.encrypt(password=secret_struct.password, user=secret_struct.user)

    dir_uri= os.environ.get("SECRETS_FS_URI")
    _, source_dir, _ = services.secrets.file_uri_parse(source_uri=dir_uri)

    file_path = f"{source_dir}{org}/{secret_struct.name}.gpg"

    with open(file_path, "wb") as f:
        f.write(crypt_struct.data)

    logger.info(f"{context.rid_get()} secrets org '{org}' create file '{file_path}' ok")

    response = fastapi.responses.JSONResponse(content={"response": "ok"})
    response.headers["HX-Redirect"] = f"/secrets/orgs/{org}"

    return response


@app.get("/secrets/orgs/{org}/generate", response_class=fastapi.responses.JSONResponse)
def secrets_org_generate(
    request: fastapi.Request,
    org: str,
):
    logger.info(f"{context.rid_get()} secrets org '{org}' generate")

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
