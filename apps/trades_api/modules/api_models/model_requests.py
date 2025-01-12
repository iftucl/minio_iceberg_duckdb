from typing import Optional, Literal
from pydantic import BaseModel, Field, validator
import datetime


class RequestTradeSubmit(BaseModel):
     DateTime: Optional[datetime.datetime] = Field(description="Timestamp for trade submission")
     Trader: str = Field(description="Trader unique Identifier")
     ISIN: str = Field(description="Instrument unique identifier", max_length=12)
     Quantity: float = Field(description="Number of instruments bought or sold", decimal_places=0, gt=0)
     Notional: float = Field(description="Monetary value of instruments bought or sold", decimal_places=0, gt=0)
     TradeType: Literal["BUY", "SELL"] = Field(description="If the trade submitted is a buy or a sell")
     Ccy: Literal["GBP", "USD"] = Field(description="We accept trades in few selected ccy: USD and GBP only")
     Counterparty: str = Field(description="The counterparty against which we are dealing this transaction")
     TradeId: Optional[str] = None

     
     class Config:
        validate_assignment = True

     @validator("DateTime", pre=True, always=True)
     def set_datetime_utcnow(cls, v):
          return datetime.datetime.now()
     
     @validator("TradeId", pre=True, always=True)
     def set_trade_id(cls, v, values):
          trisn = values.get('TradeType') + values.get('Trader') + values.get('ISIN') + values.get('DateTime').strftime('%Y%m%d%H%M%S')                
          return str(trisn)

