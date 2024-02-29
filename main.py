import uvicorn
from typing import Union
from fastapi import Depends, FastAPI, Request, HTTPException, Header
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import os
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
if "PORT" not in os.environ.keys():
    port = 8000
else:
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
key_query_scheme = APIKeyHeader(name="key")


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


class MyPayload(BaseModel):
    text_field: str
    integer_field: int | None = None


@app.post("/post-something")
async def post_something(payload: MyPayload, dependencies=Depends(required_headers)):
    """POST Something."""
    
    # do something with input_data
    new_string = payload.text_field = str(payload.integer_field)
    
    return JSONResponse(status_code=200, content={"message": "Success", "new_string": new_string})


@app.get("/get-something")
async def kobo_to_121(request: Request, api_key: str = Depends(key_query_scheme)):
    """GET Something."""

    # check API key
    if api_key != os.environ["API_KEY"]:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return JSONResponse(status_code=200, content={"data": "blablabla"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(port), reload=True)
