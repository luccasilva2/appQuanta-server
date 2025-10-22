from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from services.supabase_service import SupabaseService
from typing import Optional

class AuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        token = self._extract_token(request)

        if token:
            user_id = SupabaseService.verify_token(token)
            if user_id:
                scope["state"]["user"] = user_id
            else:
                response = JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "message": "Invalid authentication token.",
                        "data": None
                    }
                )
                await response(scope, receive, send)
                return
        else:
            # For protected routes, require token
            if self._is_protected_route(request.url.path):
                response = JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "message": "Authentication token required.",
                        "data": None
                    }
                )
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)

    def _extract_token(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            return authorization.split(" ")[1]
        return None

    def _is_protected_route(self, path: str) -> bool:
        # Define protected routes
        protected_prefixes = ["/api/v1/apps"]
        return any(path.startswith(prefix) for prefix in protected_prefixes)
