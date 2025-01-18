from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from modules.api_models import ResponseTradeSubmit, RequestTradeSubmit
from modules.middleware_helper.access_endpoints import is_trading, TraderUser
from modules.utils.api_logger import local_logger

router = APIRouter()

@router.post("/submit_trade", response_model=ResponseTradeSubmit, status_code=201)
async def submit_one_trade(request_data: RequestTradeSubmit, trader_user: TraderUser = Depends(is_trading), security=[{"bearerAuth": []}]):
    print(trader_user.trader_user)
    raise NotImplementedError

@router.get("/submit_trade", response_model=ResponseTradeSubmit, status_code=200)
async def submit_one_trade(trader_user: TraderUser = Depends(is_trading), security=[{"bearerAuth": []}]):
    local_logger.info(f"GET Request processed for trader username {trader_user.trader_user}")
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"response_body": "ok"}))
    