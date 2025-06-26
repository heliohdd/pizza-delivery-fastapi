from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db_session
from models import Order
from schemas import OrderSchema

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def get_orders():
    '''Endpoint for system standard orders. All orders router need to be authenticated.'''
    return {"message": "List of orders"}

@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_db_session)):
    '''Endpoint for creating a new order.'''
    new_order = Order(user_id=order_schema.user_id)
    session.add(new_order)
    session.commit()
    return {"message": "Order created successfully", "order id:": new_order.id}