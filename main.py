from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from endpoints.api import theRouter
from config import settings

app = FastAPI(title=settings.title, docs_url=None, redoc_url=None)

def customOpenApi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.title,
        version=settings.version,
        description=settings.description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": ""
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = customOpenApi
app.include_router(theRouter)