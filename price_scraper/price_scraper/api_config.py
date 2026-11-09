
import os

PORT = os.getenv("PORT", "8000")

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    f"http://127.0.0.1:{PORT}/api/v1"
).rstrip("/")
