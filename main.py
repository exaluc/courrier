from datetime import datetime, time, timedelta
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
import uuid

title = "Courrier"
description = "Custom email api"
version = "1.0.0"

app = FastAPI(title=title, docs_url=None, redoc_url=None)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/docs", include_in_schema=False)
def overridden_swagger():
	return get_swagger_ui_html(
     openapi_url="/openapi.json", 
     title=app.title + " - Swagger UI",
     swagger_favicon_url=""
     )

@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
	return get_redoc_html(
     openapi_url="/openapi.json", 
     redoc_favicon_url="",
     title=app.title + " - ReDoc"
     )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=title,
        version=version,
        description=description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": ""
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi