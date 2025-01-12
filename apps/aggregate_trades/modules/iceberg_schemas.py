from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType, LongType


trades_schema = Schema(
    NestedField(1, "username", StringType(), required=False),
    NestedField(2, "product", StringType(), required=False),
    NestedField(3, "quantity", LongType(), required=False)
)
