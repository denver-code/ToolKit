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


class User(BaseModel):
    email: str
    password: str

    @validator("email")
    def email_regex(cls, v):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not re.fullmatch(regex, v):
            raise ValueError("Invalid email")
        return v

    @validator("password")
    def password_hash_checker(cls, v):
        regex = r"^[a-fA-F0-9]{64}$"
        if not re.fullmatch(regex, v):
            raise ValueError("Invaid password hash")
        return v


users = []


@app.post("/signup")
async def signup(user: User):
    # REPLACE THIS SHIT..
    if user.dict() in users:
        raise HTTPException(status_code=403, detail="User already exist")
    users.append(user.dict())

    jwt_token = await ToolKit().FastJWT().encode(optional_data={"email": user.dict()["email"]})
    return {"token": jwt_token}


@app.post("/signin")
async def signin(user: User):
    # REPLACE THIS SHIT PLS..
    if user.dict() not in users:
        raise HTTPException(status_code=404, detail="User not found or password is invalid")
    for usr in users:
        if user.dict() == usr:
            jwt_token = await ToolKit().FastJWT().encode(optional_data={"email": user.dict()["email"]})
            return {"token": jwt_token}


@app.get("/secure", dependencies=[Depends(ToolKit().FastJWT().login_required)])
async def secure_page():
    return {"message": "Welcome on secure page!"}