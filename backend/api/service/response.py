from typing import Any

from fastapi.responses import JSONResponse


def format_response(status_code=200, data: Any = None):
    return JSONResponse({
        "status_code": status_code,
        "response": data
    })
