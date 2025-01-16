from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType, LongType, TimestampType


trades_schema = Schema(
    NestedField(1, "trader", StringType(), required=True),
    NestedField(2, "isin", StringType(), required=True),
    NestedField(3, "quantity", LongType(), required=True),
    NestedField(4, "notional", LongType(), required=True),
    NestedField(5, "trade_type", StringType(), required=True),
    NestedField(6, "currency", StringType(), required=True),
    NestedField(7, "counterparty", StringType(), required=True),
    NestedField(8, "trade_id", StringType(), required=True),
    NestedField(9, "business_date", TimestampType(), required=True),
)
