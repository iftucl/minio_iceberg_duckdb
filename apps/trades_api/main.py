import uvicorn
import os
from modules import app

# wip add os.environ to export main config from yaml
if os.getenv("ENV_TYPE") == "DOCKER_DEV":
    os.environ["MONGODB_URL"] = "mongodb_ice:27017"
    os.environ["MINIO_URL"] = "minioice:9000"
else:
    os.environ["MONGODB_URL"] = "localhost:27018"
    os.environ["MINIO_URL"] = "localhost:9000"

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8010)