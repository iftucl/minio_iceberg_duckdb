from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType, LongType
from pyiceberg.table import Table
import pyarrow as pa


from modules.iceberg_client import IcebergClient
from modules.iceberg_schemas import trades_schema
# name
# Configure the catalog
catalog = IcebergClient(ice_api="http://iceberg_rest:8181",
                        ice_host_uri="http://minio:9000",
                        username="ift_bigdata",
                        password="minio_password")

catalog.create_namespace_if_not_exists("trades")
# Define the schema
table = catalog.create_table_if_not_exists(
    "trades.granular_trades_",
    schema=trades_schema,
    location="s3://icebergwarehouse/trades/granular_trades_"
)

con = table.scan().to_duckdb(table_name="sales")
aggregate_df = con.execute("SELECT product, SUM(quantity) AS total_quantity FROM sales GROUP BY product").df()

