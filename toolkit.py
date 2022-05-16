import jwt
import datetime
import uuid
import secrets
from random import randint

from fastapi import HTTPException, Header


class ToolKit:
    def __init__(self):
        pass

    class Generate:
        def __init__(self):
            pass

        async def uuid4(hex=False):
            if hex:
                return uuid.uuid4().hex
            return uuid.uuid4()

        async def random_code(min=None, max=None):
            if min and max:
                return randint(min, max)
            return randint(1000, 9999)
        
        def list_selector(array):
            return secrets.choice(array)

    class FastJWT:
        def __init__(self):
            self.secret_key = ""

        def set_secret_key(self, secret_key):
            self.secret_key = secret_key

        async def encode(self, optional_data=None, expire=None):
            if not expire:
                expire = (datetime.datetime.now() + datetime.timedelta(days=30)).timestamp()

            token_json = {
                "expire": expire
            }

            if optional_data:
                token_json.update(optional_data)

            jwt_token = jwt.encode(token_json, self.secret_key, algorithm="HS256")

            return jwt_token
        

        async def decode(self, payload):
            return jwt.decode(payload, self.secret_key, algorithms=["HS256"])


        async def login_required(self, Authorization=Header("Authorization")):
            try:
                if Authorization == "Authorization":
                    raise
                
                jwt_token = await self.decode(Authorization)

                if jwt_token["expire"] < int(datetime.datetime.now().timestamp()):
                    raise

            except:
                raise HTTPException(status_code=401, detail="Unauthorized")

