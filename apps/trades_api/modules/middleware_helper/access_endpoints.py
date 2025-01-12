from fastapi import Depends, HTTPException, Request, status
from modules.api_models.model_auth import TraderAuthToken
from pydantic import BaseModel


class TraderUser(BaseModel):
    trader_user: str
    trader_group: str

def is_user(request: Request):
    user = [y for x, y in request.headers.items() if x == "X-Trader-User"]
    group = [y for x, y in request.headers.items() if x == "X-Trader-Groups"]
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return TraderUser(trader_user=user, trader_group=group)

def is_trading(user_details: TraderUser = Depends(is_user)):
    if not user_details.trader_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"response": "Not enough privileges to acces this end point"})
    return user_details