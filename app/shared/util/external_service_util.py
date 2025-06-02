import json
import os

backend_url_static_part = (os.environ["BACKEND_BASE_URL"]
                           + os.environ["BACKEND_API_PATH_PREFIX"]
                           + os.environ["BACKEND_API_PATH_VERSION"])

backend_common_headers = {
    "Content-Type": "application/json"
}


def parse_response_content(content: [bytes]) -> dict:
    body_str = content.decode("utf-8")
    return json.loads(body_str)
