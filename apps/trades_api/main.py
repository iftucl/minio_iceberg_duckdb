import uvicorn
import os
from modules import app
from ift_global.utils.read_yaml import ReadConfig


# wip add os.environ to export main config from yaml
if os.getenv("ENV_TYPE", "") == "DOCKER_DEV":
    file_config = ReadConfig("dev")
    os.environ["MONGODB_URL"] = file_config["mongodb_url"]
    os.environ["MINIO_URL"] = file_config["minio_url"]
else:
    file_config = ReadConfig("local")
    os.environ["MONGODB_URL"] = file_config["mongodb_url"]
    os.environ["MINIO_URL"] = file_config["minio_url"]

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8010)