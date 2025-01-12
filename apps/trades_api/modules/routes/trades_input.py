from fastapi import APIRouter

from modules.api_models import ResponseTradeSubmit, RequestTradeSubmit

router = APIRouter()

@router.post("/submit_trade", response_model=ResponseTradeSubmit, status_code=201)
async def submit_one_trade(request_data: RequestTradeSubmit):
    raise NotImplementedError