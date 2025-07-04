from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db_session, token_verify
from schemas import OrderItemSchema, OrderSchema
from models import Order, OrderItem, User

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
async def cancel_order(order_id: int, session: Session = Depends(get_db_session), user: User=Depends(token_verify)):
    '''Endpoint for canceling an order.'''
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not user.admin and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to cancel this order")
    order.status = "CANCELED"
    session.commit()
    return {"message": f"Order number: {order.id} canceled successfully", "order:": order}

@order_router.get("/list")
async def list_orders(session: Session = Depends(get_db_session), user: User = Depends(token_verify)):
    '''Endpoint for listing all orders.'''
    if not user.admin:
        raise HTTPException(status_code=403, detail="You do not have permission to view all orders")
    else:
        orders = session.query(Order).all()
        return {"orders": orders}
    
@order_router.post("/order/add_item/{order_id}")
async def add_item_to_order(order_id: int,
                            order_Item_Schema: OrderItemSchema,
                            session: Session = Depends(get_db_session),
                            user: User = Depends(token_verify)):
    '''Endpoint for adding an item to an order.'''
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not user.admin and order.user_id != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to add items to this order")
    order_item = OrderItem(order_Item_Schema.quantity, order_Item_Schema.flavor, order_Item_Schema.size, order_Item_Schema.unity_price, order_id)

    order.calculate_total_price()
    session.add(order_item)
    session.commit()
    return {"message": "Item added to order successfully", "item id:": order_item.id, "order price:": order.price}