import uvicorn
from typing import Union
from fastapi import Security, Depends, FastAPI, APIRouter, Request, HTTPException, Header
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from enum import Enum
import requests
import os
from enum import Enum
import base64
import logging
import sys
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
from dotenv import load_dotenv
load_dotenv()

# load environment variables
port = os.environ["PORT"]

# initialize FastAPI
app = FastAPI(
    title="fastapi-template",
    description="Template repo for FastAPI.",
    version="0.0.1",
    license_info={
        "name": "AGPL-3.0 license",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    },
)


def some_function():
    """some function that does something."""


def required_headers(
        username: str = Header(),
        password: str = Header()):
    """Headers required to use the API."""
    return username, password


@app.get("/", include_in_schema=False)
async def docs_redirect():
    """Redirect base URL to docs."""
    return RedirectResponse(url='/docs')


@app.post("/post-something")
async def post_something(request: Request, dependencies=Depends(required_headers)):
    """POST Something."""

    input_data = await request.json()
    
    # do something with input_data
    # ...
    
    return JSONResponse(status_code=200, content={"message": "Success"})


@app.get("/get-something")
async def kobo_to_121(request: Request, dependencies=Depends(required_headers)):
    """GET Something."""

    return JSONResponse(status_code=200, content={"data": "blablabla"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(port), reload=True)
