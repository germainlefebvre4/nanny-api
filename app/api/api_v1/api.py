from fastapi import APIRouter

from app.api.api_v1.endpoints import day_types, contracts, working_days, login, users, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(day_types.router, prefix="/day_types", tags=["day_types"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["contracts"])
api_router.include_router(working_days.router, prefix="/working_days", tags=["working_days"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
