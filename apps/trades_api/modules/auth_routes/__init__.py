from fastapi import APIRouter

from modules.auth_routes.auth_route import router as auth_users

auth_router = APIRouter()
auth_router.include_router(auth_users, tags=["auth"])