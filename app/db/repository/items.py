from sqlalchemy.orm import Session
from ...schemas.items import ItemCreate, ItemUpdate
from ..models.items import Item

def create_new_item(item: ItemCreate, db: Session):
    item = Item(
        name = item.name,
        cost = item.cost,
        available_quantity = item.available_quantity
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def list_items(db: Session):
    items = db.query(Item).all()
    return items

def retrieve_item(id: int, db: Session):
    item = db.query(Item).filter(Item.id == id).first()
    return item

def update_item_by_id(id: int, item: ItemUpdate, db: Session):
    existing_item = db.query(Item).filter(Item.id == id)
    if not existing_item.first():
        return 0
    first_existing_item = existing_item.first()
    for var, value in vars(item).items():
        setattr(first_existing_item, var, value) if value else None

    db.add(first_existing_item)
    db.commit()
    return 1

def delete_item_by_id(id: int, db: Session):
    existing_item = db.query(Item).filter(Item.id == id)
    if not existing_item.first():
        return 0
    existing_item.delete(synchronize_session = False)
    db.commit()
    return 1
