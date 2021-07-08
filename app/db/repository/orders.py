from sqlalchemy.orm import Session
from ...schemas.orders import OrderCreate, OrderUpdate
from ..models.orders import Order

def create_new_order(order: OrderCreate, db: Session):
    order = Order(
        shopping_cart_id = order.shopping_cart_id,
        requested_quantity = order.requested_quantity,
        total_cost = order.total_cost,
        item_id = order.item_id
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def list_orders(db: Session):
    orders = db.query(Order).all()
    return orders

def retrieve_order(id: int, db: Session):
    order = db.query(Order).filter(Order.id == id).first()
    return order

def update_order_by_id(id: int, order: OrderCreate, db: Session):
    existing_order = db.query(Order).filter(Order.id == id)
    if not existing_order.first():
        return 0
    first_existing_order = existing_order.first()
    for var, value in vars(order).items():
        setattr(first_existing_order, var, value) if value else None

    db.add(first_existing_order)
    db.commit()
    return 1

def delete_order_by_id(id: int, db: Session):
    existing_order = db.query(Order).filter(Order.id == id)
    if not existing_order.first():
        return 0
    existing_order.delete(synchronize_session = False)
    db.commit()
    return 1
