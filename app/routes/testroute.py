from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.core.db import get_db
from sqlalchemy.orm import Session
from app.models.testroute import Items,ItemRequestModel, ItemResponseModel

router = APIRouter()

@router.get(
    "/items",
    description="get items",
    operation_id="getItems",
    response_model=List[ItemResponseModel]
)
async def get_items(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, le=100, description="Maximum number of records to return"),
    title: Optional[str] = Query(None, description="Filter by title (partial match)"),
    db: Session = Depends(get_db)):
    """
    get all items.
    """
    try:
        query = db.query(Items)
        if title:
            query = query.filter(Items.title.ilike(f"%{title}%"))
        items_results = query.offset(skip).limit(limit).all()
    
        return items_results
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )
    

# --------------------------------------------------------------------
# GET /items/{id} — Retrieve single item
# --------------------------------------------------------------------
@router.get(
    "/items/{id}",
    description="get items by id",
    summary="Get item by ID",
    response_model=ItemResponseModel
)
async def get_items(id: int,db: Session = Depends(get_db)):
    """
    get item by id
    """
    try:
        item = db.query(Items).filter(Items.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )

# --------------------------------------------------------------------
# POST /items — Create new item
# --------------------------------------------------------------------
@router.post("/items", 
                response_model=ItemResponseModel,
                status_code=HTTP_201_CREATED)
def create_item(payload: ItemRequestModel, 
                db: Session = Depends(get_db)):
    """
    Create a new item
    """
    try:
        existing = db.query(Items).filter(Items.title == payload.title).first()
        if existing:
            raise HTTPException(status_code=400, detail="Item with this title already exists.")
    
        new_item = Items(**payload.model_dump())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )

# --------------------------------------------------------------------
# PUT /items/{id} — Update item
# --------------------------------------------------------------------
@router.put("/items/{id}",
        operation_id="updateItem",
        response_model=ItemResponseModel)
def update_item(id: int, 
    payload: ItemRequestModel, 
    db: Session = Depends(get_db)
    ):
    """
    Update an existing item
    """
    try:
        item = db.query(Items).filter(Items.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)
        return item
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )

# --------------------------------------------------------------------
# DELETE /items/{id} — Delete item
# --------------------------------------------------------------------
@router.delete("/items/{item_id}", 
               summary="Delete an item by ID",
               status_code=HTTP_204_NO_CONTENT
            )
def delete_item(
    item_id: int, 
    db: Session = Depends(get_db)
    ):
    """
    Delete an item by ID
    """
    try:
        item = db.query(Items).filter(Items.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(item)
        db.commit()
        return None
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}",
        )
    


