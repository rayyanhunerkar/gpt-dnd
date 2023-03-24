from collections import defaultdict

from app.database.db import session
from fastapi import FastAPI
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .configs.settings import ProjectSettings
from .routes.user import auth_router

app = FastAPI(
    title=ProjectSettings.title,
    debug=ProjectSettings.debug,
    root_path_in_servers=ProjectSettings.root_path,
    openapi_url=f'{ProjectSettings.root_path}/openapi.json',
    docs_url=f'{ProjectSettings.root_path}/docs',
    redoc_url=f'{ProjectSettings.root_path}/redoc',
    version=ProjectSettings.version
)

app.mount(ProjectSettings.root_path, app)


@app.exception_handler(RequestValidationError)
async def custom_form_validation_error(request, exc):
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(str(filtered_loc))  # nested fields with dot-notation
        reformatted_message[field_string].append(msg)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"detail": "Invalid request", "errors": reformatted_message}
        ),
    )


@app.on_event("startup")
async def startup():
    await session.create_all()


@app.on_event("shutdown")
async def shutdown():
    await session.close()


@app.get("/ping", status_code=status.HTTP_200_OK)
async def health() -> str:
    return "pong"


app.include_router(auth_router)
