from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db_session, token_verify
from models import Order
from schemas import OrderSchema

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(token_verify)])

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

@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_db_session)):
    '''Endpoint for canceling an order.'''
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "CANCELED"
    session.commit()
    return {"message": "Order canceled successfully", "order id:": order_id}