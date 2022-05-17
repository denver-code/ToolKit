import re
from toolkit import ToolKit

from functools import wraps

from fastapi import (
    FastAPI,
    HTTPException,
    Depends
)

from pydantic import (
    BaseModel,
    validator
)

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="FastAPI", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ToolKit().FastJWT().set_secret_key("SUPERSECRETKEY")

@app.get("/")
async def index_page():
    return {"Hello": "World"}