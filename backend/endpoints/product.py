from typing import List, Optional

from fastapi import BackgroundTasks, Depends, File, Form, UploadFile
from motor.core import AgnosticDatabase
from odmantic import ObjectId

from backend import controllers, deps, schemas
from backend.custom_router import router
from backend.services import firebase_storage, notification

router.tags = ["product"]


@router.post("/product", response_model=schemas.Product)
async def post_product(
    background_tasks: BackgroundTasks,
    description: Optional[str] = Form(default=""),
    name: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...),
    db: AgnosticDatabase = Depends(deps.get_db),
    superuser=Depends(deps.get_current_superuser),
):
    image_url = await firebase_storage.upload_image_to_firestore(image)
    product_in = schemas.ProductCreate(
        name=name, image=image_url, description=description, price=price
    )
    product = await controllers.product.create(db=db, obj_in=product_in)

    background_tasks.add_task(
        notification.send_notification,
        f"the marketplace has listed a new product {product.name}",
        "product",
    )
    return product


@router.get("/product/all", response_model=List[schemas.ProductCompact])
async def get_products(db: AgnosticDatabase = Depends(deps.get_db)):
    return await controllers.product.get_multi(db=db)


@router.get("/product/{product_id}", response_model=schemas.Product)
async def get_product_by_id(
    product_id: ObjectId, db: AgnosticDatabase = Depends(deps.get_db)
):
    return await controllers.product.get(db=db, id=product_id)
