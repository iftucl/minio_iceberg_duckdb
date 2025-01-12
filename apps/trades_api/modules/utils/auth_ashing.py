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
from modules.api_models import TraderAuthRequest, TraderAuthToken

SECRET_KEY = "7b5307fa3b4617893a6a9ff4231a6f73cfba39910bc95d6ece2867e465a84852" # used for jwt created as "openssl rand -hex 32" from bash terminal
ENC_ALGORITHM = "HS256" # used for jwt
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def authenticate_user(auth_data: TraderAuthRequest) -> bool:
    """
    Examples:
        >>> import asyncio
        >>> loop = asyncio.get_event_loop()
        >>> loop.run_until_complete(authenticate_user(username="foo", password="$2b$12$a5/vV5u5q6zXUvaZzh9jF.lYvi5qGpVteLqGKM.mWyetCXQwCqV9e"))
    """
    user = await get_user(auth_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.password != auth_data.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not Authenticated")
    return auth_data
    
def create_token(data: TraderAuthRequest, expires_delta: timedelta | None = None):    

    if expires_delta:
        expires = datetime.now() + expires_delta
    else:
        expires = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    auth_data = TraderAuthToken(username=data.username, password=data.password, email=data.email, token_expiry=expires)
    
    encoded_jwt = jwt.encode(jsonable_encoder(auth_data), SECRET_KEY, algorithm=ENC_ALGORITHM)
    return encoded_jwt

def get_user_from_token(token: str = Depends(oauth_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='could not validate credentials',
                                         headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ENC_ALGORITHM])
        token_data = TraderAuthToken(**payload)
    except JWTError:
        raise credential_exception        
    except ValidationError as exc:
        print(repr(exc.errors()[0]['type']))
        raise HTTPException(status_code=400, detail='Inactive User')
    print(token_data)
    return token_data
   
