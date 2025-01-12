from pydantic import BaseModel, Field
from typing import Literal


class ResponseTradeSubmit(BaseModel):
    trade_status: Literal["accepted", "rejected", "requires_validation"] = Field(description="Trade Status")
