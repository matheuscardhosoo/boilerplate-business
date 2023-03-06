import logging
from time import time
from typing import Awaitable, Callable, Type

from fastapi import APIRouter, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware


class FastapiManager:
    """Manager for FastAPI"""

    def __init__(self, app: FastAPI):
        self._logger = logging.getLogger(f"{self.__class__.__name__}")
        self._app = app
        self._app.router.route_class = APIRoute

    def include_router(self, router: APIRouter, name: str) -> None:
        self._app.include_router(router)
        self._logger.info(f"Included {name} Router!")

    def add_exception_handler(self, exception: Type[Exception], func: Callable) -> None:
        self._app.add_exception_handler(exception, func)
        self._logger.info(f"Added {exception.__name__} Handler [{func.__name__}]!")

    def add_event_handler(self, event_type: str, func: Callable) -> None:
        self._app.add_event_handler(event_type, func)
        self._logger.info(f"Added {event_type} Handler [{func.__name__}]!")

    def add_middleware(self, func: Callable) -> None:
        self._app.add_middleware(BaseHTTPMiddleware, dispatch=func)
        self._logger.info(f"Added HTTP Middleware [{func.__name__}]!")

    def generate_middleware_dispatch(self) -> Callable:
        """Generate a function to be used as hook in HTTP layer."""

        async def dispatch(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
            """Hook to be executed in HTTP layer."""
            transaction_id = request.headers.get("x-transaction-id")
            start_time = time()
            try:
                response = await call_next(request)
            except Exception as error:
                process_time = time() - start_time
                msg = "%s %s %s X-Process-Time: %s X-Transaction-ID: %s"
                code = error.status_code if isinstance(error, HTTPException) else 500
                self._logger.warning(
                    msg, code, request.method, request.url, process_time, transaction_id, exc_info=True
                )
                raise
            process_time = time() - start_time
            msg = "%s %s %s - X-Process-Time: %s - X-Transaction-ID: %s"
            self._logger.info(msg, response.status_code, request.method, request.url, process_time, transaction_id)
            response.headers["X-Process-Time"] = str(process_time)
            return response

        return dispatch

    @staticmethod
    async def exception_handler(request: Request, exc: Exception) -> Response:
        """Build a JSON Response for given exception"""
        content = {"detail": getattr(exc, "detail")}
        headers = {"x-transaction-id": request.headers.get("x-transaction-id", "")}
        return JSONResponse(status_code=getattr(exc, "code"), content=content, headers=headers)
