import uvicorn
import os
from modules import app

# wip add os.environ to export main config from yaml
os.environ["MONGODB_URL"] = "localhost:27018"
os.environ["MINIO_URL"] = "localhost:27018"


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8010)