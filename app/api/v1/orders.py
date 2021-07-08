from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...schemas.orders import OrderCreate, OrderUpdate
from ...db.session import get_db
from ...db.repository.orders import create_new_order, list_orders, retrieve_order, update_order_by_id, delete_order_by_id
from ...db.repository.items import retrieve_item

router = APIRouter()

@router.post("/")
def create(order: OrderCreate, db: Session = Depends(get_db)):
    item = retrieve_item(order.item_id, db)
    if not item:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Order with this id {order.item_id} does not exist")
    if int(order.requested_quantity) > int(item.available_quantity):
        raise HTTPException(status_code = 422, detail = f"Order quantity cannot be more than {item.available_quantity}")
    order = create_new_order(order, db)
    return order

@router.get("/")
def find(db:Session = Depends(get_db)):
    orders = list_orders(db=db)
    return orders

@router.get("/{id}")
def find_by_id(id: int, db: Session = Depends(get_db)):
    order = retrieve_order(id, db)
    if not order:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Order with this id {id} does not exist")
    return order

@router.put("/{id}")
def update(id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    if order.item_id:
        new_item = retrieve_item(order.item_id, db)
        if not new_item:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Order with this id {order.item_id} does not exist")
    if order.requested_quantity:
        old_order = retrieve_order(id, db)
        old_item = retrieve_item(old_order.item_id, db)
        if int(order.requested_quantity) > int(old_item.available_quantity):
            raise HTTPException(status_code = 422, detail = f"Order quantity cannot be more than {old_item.available_quantity}")
    message = update_order_by_id(id, order, db)
    if not message:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"Order with id {id} not found")
    return {"msg":"Successfully updated data."}

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    message = delete_order_by_id(id, db)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order with id {id} not found")
    return {"msg":"Successfully deleted."}
