from typing import Any, Dict, Union

from motor.core import AgnosticDatabase

from backend.controllers.base import BaseController
from backend.models.user import User
from backend.schemas.user import UserCreate, UserUpdate
from backend.security import get_password_hash, verify_password


# ODM, Schema, Schema
class UserController(BaseController[User, UserCreate, UserUpdate]):

    async def get_by_email(
        self, db: AgnosticDatabase, *, email: str
    ) -> User | None:
        return await self.engine.find_one(User, User.email == email)

    async def create(
        self, db: AgnosticDatabase, *, obj_in: UserCreate
    ) -> User:

        user = {
            **obj_in.model_dump(),
            "email": obj_in.email,
            "password": (
                get_password_hash(obj_in.password)
                if obj_in.password is not None
                else None
            ),
            "is_superuser": obj_in.is_superuser,
        }

        return await self.engine.save(User(**user))

    async def authenticate(
        self, db: AgnosticDatabase, *, email: str, password: str
    ) -> User | None:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(
            plain_password=password, password=user.password
        ):
            return None
        return user

    async def update(
        self,
        db: AgnosticDatabase,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            update_data["password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    @staticmethod
    def has_password(user: User) -> bool:
        return user.password is not None

    @staticmethod
    def is_active(user: User) -> bool:
        return user.is_active

    @staticmethod
    def is_superuser(user: User) -> bool:
        return user.is_superuser


user = UserController(User)
