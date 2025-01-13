FROM python:3.10-bullseye

COPY --chmod=770 . /home/minio_iceberg_duckdb

RUN pip install poetry

RUN cd /home/minio_iceberg_duckdb && poetry install --all-extras

CMD cd /home/apps/trades_api && poetry run uvicorn main:app --workers 8 --port 8010 --host 0.0.0.0