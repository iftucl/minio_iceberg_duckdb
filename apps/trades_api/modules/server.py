from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware


#from modules.auth_module.middleware_helper import CustomAuthBackend, CheckPermissionsMiddleware
from modules.auth_routes import auth_router
from modules.routes import trades_router

def get_application():
    app = FastAPI(debug=True, 
                  title="trades_api",
                  version="0.0.0", 
                  description="Trade Portal APIs",                  
                  middleware=[
                      Middleware(TrustedHostMiddleware, allowed_hosts=["*"]),
                      Middleware(SessionMiddleware, secret_key="your-secret-key"),
                      #Middleware(AuthenticationMiddleware, backend=CustomAuthBackend()),
                      #Middleware(CheckPermissionsMiddleware),
                      ]
                )    
    # Add CORS middleware
    # Add custom authentication middleware with custom error handler
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Include API routes
    app.include_router(auth_router)
    app.include_router(trades_router)
    
    return app

app = get_application()