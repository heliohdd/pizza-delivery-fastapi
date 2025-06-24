from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def get_orders():
    '''Endpoint for system standard orders. All orders router need to be authenticated.'''
    return {"message": "List of orders"}