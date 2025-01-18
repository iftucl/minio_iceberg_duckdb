from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser, UnauthenticatedUser
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from jose import JWTError
from datetime import datetime

from modules.utils.auth_ashing import get_user_from_token
from modules.utils.api_logger import local_logger

class CustomAuthMiddleware(AuthenticationBackend):
    async def authenticate(self, request):
        try:
            if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json") or request.url.path in ["/token", "/login", "/signup"]:
                return None
            token = request.headers.get("authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Missing authentication token")            
            try:
                token = token.split("Bearer ")[1]
                payload = get_user_from_token(token=token)
                if payload.username is None:
                    raise HTTPException(status_code=401, detail="Invalid authentication token")
                if payload.token_expiry < datetime.now():
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token has expired")
            except JWTError:
                raise HTTPException(status_code=401, detail="Invalid authentication token")
        except Exception as exc:
            local_logger.error(f"Error as : {exc}")
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="Forbidden Middleware Auth")
        
        return AuthCredentials(scopes="admin"), SimpleUser(payload.username)
    
class CheckPermissionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            if isinstance(request.user, UnauthenticatedUser):
                return JSONResponse(status_code=status.HTTP_403_FORBIDDEN)
            set_groups = set(request.auth.scopes)
            request.scope["headers"].append((b"X-Traders-Groups", "ADMIN"))
            request.scope["headers"].append(b"X-Trader-User", request.user)
            response = await call_next(request)
            return response
        except Exception as exc:
            print(f"error as : {exc}")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Error in auth groups")