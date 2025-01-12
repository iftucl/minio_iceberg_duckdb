from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from datetime import timedelta, datetime
from modules.utils.mongo_connect import get_user
from jose import jwt, JWTError # use python-jose rather than jose
from pydantic import ValidationError

#from app.data_models.token_models import TokenData
#from app.data_models.db_users import UserInDb
from modules.utils.ashing_utils import HashingTool
from modules.api_models import MongoTraderToken

SECRET_KEY = "7b5307fa3b4617893a6a9ff4231a6f73cfba39910bc95d6ece2867e465a84852" # used for jwt created as "openssl rand -hex 32" from bash terminal
ENC_ALGORITHM = "HS256" # used for jwt
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def authenticate_user(username, password) -> bool:
    """
    Examples:
        >>> import asyncio
        >>> loop = asyncio.get_event_loop()
        >>> loop.run_until_complete(authenticate_user(username="foo", password="$2b$12$a5/vV5u5q6zXUvaZzh9jF.lYvi5qGpVteLqGKM.mWyetCXQwCqV9e"))
    """
    user = await get_user(username)
    if not user:
        return False
    if user.password != password:
        return False
    return True
    
def create_token(data: MongoTraderToken, expires_delta: timedelta | None = None):    

    if expires_delta:
        expires = datetime.now() + expires_delta
    else:
        expires = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    data.token_expiry = expires
    
    encoded_jwt = jwt.encode(jsonable_encoder(data), SECRET_KEY, algorithm=ENC_ALGORITHM)
    return encoded_jwt

def get_user_from_token(token: str = Depends(oauth_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='could not validate credentials',
                                         headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ENC_ALGORITHM])
        token_data = MongoTraderToken(**payload)
    except JWTError:
        raise credential_exception        
    except ValidationError as exc:
        print(repr(exc.errors()[0]['type']))
        raise HTTPException(status_code=400, detail='Inactive User')

    return token_data
   
