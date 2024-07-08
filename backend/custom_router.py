import inspect
import re
from typing import Any, Callable, Coroutine

from bson import ObjectId
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.routing import APIRoute


class CustomAPIRoute(APIRoute):
    """
    Makes the route available on the request object. and converts id to mongo objectId
    """

    def get_route_handler(
        self,
    ) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        handler = super().get_route_handler()

        # Check if the handler takes one param (request) or 3 (raw ASGI)
        # If it's ASGI, don't touch it
        if len(inspect.signature(handler).parameters) > 1:  # pragma: no cover
            return handler

        # Add the route to the request object and converts id
        async def wrapped_handler(request: Request) -> Response:
            request.route = self
            params = [
                param
                for param in request.path_params.keys()
                if param.endswith("_id")
            ]

            for id in params:
                if id and re.match("[0-9a-f]{24}", id):
                    request.path_params[id] = ObjectId(id)
            request.cached_body = await request.body()
            return await handler(request)

        return wrapped_handler


router = APIRouter(route_class=CustomAPIRoute)
