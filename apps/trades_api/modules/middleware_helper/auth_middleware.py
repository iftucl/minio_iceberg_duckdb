from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        
        if request.url.path in ["/token", "/login", "/signup"]:
            return await call_next(request)
        
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Missing authentication token")
        
        try:
            token = token.split("Bearer ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid authentication token")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        
        return await call_next(request)
