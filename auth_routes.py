from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    '''Endpoint for system standard authentication'''
    return {"message": "Auth endpoint"}