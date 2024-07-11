from typing import List

from fastapi import Body, Depends, HTTPException, status
from motor.core import AgnosticDatabase
from odmantic import ObjectId
from pydantic import EmailStr

from backend import controllers, deps, models, schemas
from backend.custom_router import router

router.tags = ["user"]


@router.post("/register", response_model=schemas.UserInDB)
async def create_user(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
):
    """
    Create new user without the need to be logged in.
    """

    user = await controllers.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="This username is not available.",
        )

    user_in = schemas.UserCreate(password=password, email=email)
    user = await controllers.user.create(db, obj_in=user_in)
    return user


@router.get("/user", response_model=schemas.UserInDB)
async def get_user(
    *,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    For testing
    """

    return current_user


@router.post("/add-to-cart/{product_id}", response_model=schemas.Msg)
async def add_to_cart(
    product_id: ObjectId,
    current_user: models.User = Depends(deps.get_current_user),
    db: AgnosticDatabase = Depends(deps.get_db),
):

    if product_id in current_user.cart:
        return schemas.Msg(msg="this product is already in cart")

    product = await controllers.product.get(db=db, id=product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product was not found",
        )

    current_user.cart.append(product_id)
    await controllers.user.engine.save(current_user)
    return schemas.Msg(msg=f"{product.name} added to cart")


@router.get("/cart", response_model=List[schemas.Product])
async def get_user_cart(
    current_user: models.User = Depends(deps.get_current_user),
    db: AgnosticDatabase = Depends(deps.get_db),
):
    return await controllers.product.get_by_ids(db=db, ids=current_user.cart)
