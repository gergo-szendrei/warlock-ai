import logging
import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=os.environ["LOGGING_LEVEL"])

if __name__ == "__main__":
    uvicorn.run(
        app="app:application",
        host="127.0.0.1",
        port=8123
    )
