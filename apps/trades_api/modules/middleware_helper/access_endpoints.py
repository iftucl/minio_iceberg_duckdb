from fastapi import Depends, HTTPException, Request, status
from modules.api_models.model_auth import TraderAuthToken
from pydantic import BaseModel

from modules.utils.auth_ashing import get_user_from_token

class TraderUser(BaseModel):
    trader_user: str
    trader_group: str

def is_user(request: Request):
    token = request.headers.get("authorization")
    token = token.split("Bearer ")[1]
    payload = get_user_from_token(token=token)    
    #user = [y for x, y in request.headers.items() if x == "X-Trader-User"]
    group = "admin" #[y for x, y in request.headers.items() if x == "X-Trader-Groups"]
    if not payload.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return TraderUser(trader_user=payload.username, trader_group=group)

def is_trading(user_details: TraderUser = Depends(is_user)):
    if not user_details.trader_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"response": "Not enough privileges to access this end point"})
    return user_details