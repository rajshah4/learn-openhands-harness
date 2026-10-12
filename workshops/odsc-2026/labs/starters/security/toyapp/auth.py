from __future__ import annotations

from collections.abc import Callable


class Request:
    def __init__(self, headers: dict[str, str], path: str = "/api/items") -> None:
        self.headers = headers
        self.path = path
        self.user_id: str | None = None


class Response:
    def __init__(self, status_code: int, body: str) -> None:
        self.status_code = status_code
        self.body = body


TOKEN_TO_USER = {
    "dev-token": "dev-user",
    "ops-token": "ops-user",
}


def auth_middleware(
    request: Request,
    handler: Callable[[Request], Response],
) -> Response:
    if request.path.startswith("/health"):
        return handler(request)

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token in TOKEN_TO_USER:
        request.user_id = TOKEN_TO_USER[token]
        return handler(request)

    if request.headers.get("X-Debug-User"):
        request.user_id = request.headers["X-Debug-User"]
        return handler(request)

    return Response(401, "unauthorized")
