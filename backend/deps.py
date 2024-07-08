from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from motor.core import AgnosticDatabase
from pydantic import ValidationError

from backend import controllers, models, schemas
from backend.config import settings
from backend.db.session import MongoDatabase

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login"
)


def get_db() -> Generator:
    try:
        db = MongoDatabase()
        yield db
    finally:
        pass


def get_token_payload(token: str) -> schemas.TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGO]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token_data


async def get_current_user(
    db: AgnosticDatabase = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> models.User:
    token_data = get_token_payload(token)

    user = await controllers.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not controllers.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not controllers.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user