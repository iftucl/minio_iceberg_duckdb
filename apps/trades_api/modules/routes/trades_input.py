from fastapi import APIRouter, Depends

from modules.api_models import ResponseTradeSubmit, RequestTradeSubmit
from modules.middleware_helper.access_endpoints import is_trading, TraderUser
router = APIRouter()

@router.post("/submit_trade", response_model=ResponseTradeSubmit, status_code=201)
async def submit_one_trade(request_data: RequestTradeSubmit, trader_user: TraderUser = Depends(is_trading)):
    print(trader_user.trader_user)
    raise NotImplementedError