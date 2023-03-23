import json
import typing

from aiohttp.web_exceptions import HTTPClientError, HTTPUnprocessableEntity
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import get_session

from app.admin.dataclasses import Admin
from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request

HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPClientError as e:
        return error_json_response(
            http_status=e.status_code,
            status=HTTP_ERROR_CODES[e.status_code],
            message=e.reason,
            data=e.text,
        )
    except Exception as e:
        return error_json_response(
            http_status=500, status="internal server error", message=str(e)
        )


@middleware
async def auth_check_middleware(request: "Request", handler):
    if session := await get_session(request):
        request.admin = Admin.from_session(session)

    return await handler(request)


def setup_middlewares(app: "Application"):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(auth_check_middleware)
    app.middlewares.append(validation_middleware)
