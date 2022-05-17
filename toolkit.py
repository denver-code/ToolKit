import jwt
import datetime
import uuid
import secrets
from random import randint

from fastapi import HTTPException, Header

from toolkit_internal.exceptions import *

class ToolKit:
    def __init__(self):
        pass


    class IntFix:
        def __init__():
            pass

        
        # Maybe later I try realize it with regex :)
        async def represents_int(
            self, 
            value,
            return_value=False
        ):
            try: 

                int(value)

                if return_value:
                    return int(value)
                return True

            except ValueError:
                return False

        
        async def fix(
            self,
            value,
            fix_negative=True,
            fix_negative_only=False,
            max_value=None,
            min_value=None,
        ):
            if not await self.represents_int():
                raise InvalidRepresentOfNumber
            
            if fix_negative:
                if value < 0 and not 0:
                    value = value * -1
                
            if fix_negative_only:
                return value

            if max_value:
                if value > max_value:
                    return max_value

            if min_value:
                if value < min_value:
                    return min_value        
            
            return int(value)


    class DateGenerator:
        def __init__(self):
            pass

        
        async def get_time(value, time_format):
            avaible_formats = ["d", "m", "h", "s"]

            if not await ToolKit.IntFix.represents_int(value):
                value = 60

            if time_format == "d":
                value = (datetime.datetime.now() + timedelta(days=value)).timestamp()
            elif time_format == "m":
                value = (datetime.datetime.now() + timedelta(minutes=value)).timestamp()
            elif time_format == "h":
                value = (datetime.datetime.now() + timedelta(hours=value)).timestamp()
            else:
                value = (datetime.datetime.now() + timedelta(seconds=value)).timestamp()

    
    class Validate:
        def __init__(self):
            pass

        async def email(email):
            regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
            if not re.fullmatch(regex, email):
                raise ValueError("Invalid email")
            return email 
        

        async def hash_sha256(_hash):
            regex = r"^[a-fA-F0-9]{64}$"
            if not re.fullmatch(regex, _hash):
                raise ValueError("Invaid hash")
            return _hash
        

        async def integer(value):
            regex = r"^[-+]?[0-9]+$"
            if not re.fullmatch(regex, value):
                raise ValueError("Invaid hash")
            return value


    class Generate:
        def __init__(self):
            pass

        async def uuid4(hex=False):
            if hex:
                return uuid.uuid4().hex
            return uuid.uuid4()

        async def random_code(
            min=None,
            max=None
        ):
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

        async def encode(
            self,
            optional_data=None,
            expire=None
        ):
            if not expire:
                expire = (
                    datetime.datetime.now() + datetime.timedelta(days=30)
                ).timestamp()

            token_json = {
                "expire": expire
            }

            if optional_data:
                token_json.update(optional_data)

            jwt_token = jwt.encode(
                token_json,
                self.secret_key,
                algorithm="HS256"
            )

            return jwt_token
        

        async def decode(self, payload):
            return jwt.decode(
                payload,
                self.secret_key,
                algorithms=["HS256"]
            )


        async def login_required(self, Authorization=Header("Authorization")):
            try:
                if Authorization == "Authorization":
                    raise
                
                jwt_token = await self.decode(Authorization)

                if jwt_token["expire"] < int(datetime.datetime.now().timestamp()):
                    raise

            except:
                raise HTTPException(status_code=401, detail="Unauthorized")

