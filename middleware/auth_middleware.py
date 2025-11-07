from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from services.supabase_service import SupabaseService
from typing import Optional

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = self._extract_token(request)

        if token:
            user_id = SupabaseService.verify_token(token)
            if user_id:
                request.state.user = user_id
            else:
                print(f"Invalid token: {token[:50]}...")
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "message": "Invalid authentication token.",
                        "data": None
                    }
                )
        else:
            # For protected routes, require token
            if self._is_protected_route(request.url.path):
                print(f"No token provided for protected route: {request.url.path}")
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "message": "Authentication token required.",
                        "data": None
                    }
                )

        response = await call_next(request)
        return response

    def _extract_token(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            return authorization.split(" ")[1]
        return None

    def _is_protected_route(self, path: str) -> bool:
        # Define protected routes
        protected_prefixes = ["/api/v1/apps"]
        return any(path.startswith(prefix) for prefix in protected_prefixes)
