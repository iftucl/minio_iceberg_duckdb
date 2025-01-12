from fastapi import APIRouter

from modules.routes.trades_input import router as input_trades

trades_router = APIRouter()
trades_router.include_router(input_trades, prefix="/submit_trade", tags=["input"])