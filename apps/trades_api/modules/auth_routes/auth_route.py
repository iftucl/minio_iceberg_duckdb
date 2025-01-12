from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt
from datetime import datetime, timedelta
from modules.api_models import CreateUserRequest
from modules.utils.mongo_connect import create_user

router = APIRouter()

@router.post("/signup")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validate user credentials here
    new_user = CreateUserRequest(username=form_data.username,
                                 password=form_data.password,
                                 email=form_data.client_id)
    try:
        create_response = await create_user(new_user=new_user)
    except Exception as exc:
        print(f"Could not create new user as exception {exc}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User could not be created")
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"creation_time": create_response.inserted_id.generation_time,
                                                                                  "acknowledged": create_response.acknowledged}))

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validate user credentials here
    if form_data.username != "testuser" or form_data.password != "testpassword":
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}