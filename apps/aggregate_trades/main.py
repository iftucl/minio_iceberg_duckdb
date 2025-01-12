from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, StringType, LongType
from pyiceberg.table import Table
import pyarrow as pa

# name
# Configure the catalog
catalog = load_catalog(
    "demo",
    **{
        "uri": "http://iceberg_rest:8181",
        "s3.endpoint": "http://minio:9000",
        "s3.access-key-id": "ift_bigdata",
        "s3.secret-access-key": "minio_password",
    }
)
catalog.create_namespace_if_not_exists("demo_bd")
# Define the schema
schema = Schema(
    NestedField(1, "username", StringType(), required=False),
    NestedField(2, "product", StringType(), required=False),
    NestedField(3, "quantity", LongType(), required=False)
)

table = catalog.create_table_if_not_exists(
    "demo_bd.sales",
    schema=schema,
    location="s3://icebergwarehouse/demo/sales"
)
# Prepare data
data = [
    ("alice", "laptop", 1),
    ("bob", "mouse", 2),
    ("charlie", "keyboard", 3)
]

# Convert to PyArrow table
pa_table = pa.Table.from_pylist([{"username": u, "product": p, "quantity": q} for u, p, q in data])

# Write data to the table
table.append(pa_table)

# Read and print data
df = table.scan().to_arrow().to_pandas()
print(df)

df = table.scan().to_arrow().to_pandas()

con = table.scan().to_duckdb(table_name="sales")
aggregate_df = con.execute("SELECT product, SUM(quantity) AS total_quantity FROM sales GROUP BY product").df()


# Perform aggregation
aggregated_data = (
    table.scan()
    .to_arrow()
    .to_pandas()
    .groupby(["product"])
    .aggregate([("quantity", "sum")])
)
