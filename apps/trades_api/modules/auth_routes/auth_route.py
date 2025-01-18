from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt
from datetime import datetime, timedelta
from modules.api_models import CreateUserRequest
from modules.utils.mongo_connect import create_user
from modules.utils.auth_ashing import authenticate_user, create_token

from modules.utils.api_logger import local_logger

router = APIRouter()

@router.post("/signup")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validate user credentials here
    new_user = CreateUserRequest(username=form_data.username,
                                 password=form_data.password,
                                 email=form_data.client_id)
    local_logger.info(f"User: {new_user} requested to create new account")
    try:
        create_response = await create_user(new_user=new_user)
    except Exception as exc:
        local_logger.info(f"Could not create new user as exception {exc}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User could not be created")
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"creation_time": create_response.inserted_id.generation_time,
                                                                                  "acknowledged": create_response.acknowledged}))

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(authenticate_user)):
    access_token = create_token(data=form_data)
    return {"access_token": access_token, "token_type": "bearer"}