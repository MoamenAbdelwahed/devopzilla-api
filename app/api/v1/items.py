from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...schemas.items import ItemCreate, ItemUpdate
from ...db.session import get_db
from ...db.repository.items import create_new_item, list_items, retrieve_item, update_item_by_id, delete_item_by_id

router = APIRouter()

@router.post("/")
def create(item: ItemCreate, db: Session = Depends(get_db)):
    item = create_new_item(item, db)
    return item

@router.get("/")
def find(db:Session = Depends(get_db)):
    items = list_items(db)
    return items

@router.get("/{id}")
def find_by_id(id: int, db: Session = Depends(get_db)):
    item = retrieve_item(id, db)
    if not item:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Item with this id {id} does not exist")
    return item

@router.put("/{id}")
def update(id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    message = update_item_by_id(id, item, db)
    if not message:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id {id} not found")
    return {"msg":"Successfully updated data."}

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    message = delete_item_by_id(id, db)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id {id} not found")
    return {"msg":"Successfully deleted."}
