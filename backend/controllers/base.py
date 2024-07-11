from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from motor.core import AgnosticDatabase
from odmantic import AIOEngine
from pydantic import BaseModel

from backend.config import settings
from backend.db.base_class import Base
from backend.db.session import get_engine

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseController(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        controller object with default methods to Create, Read, Update, Delete.
        """
        self.model = model
        self.engine: AIOEngine = get_engine()

    def build_eq_query(self, args: Dict[str, Any]):
        query = []
        # Build the query dynamically, supports only eq
        for field, value in args.items():
            model_field = getattr(self.model, field)
            if not field:
                continue
            expression = model_field.eq(value)
            query.append(expression)
        return query

    async def get(self, db: AgnosticDatabase, **kwargs) -> ModelType | None:
        query = self.build_eq_query(kwargs)
        return await self.engine.find_one(self.model, *query)

    async def get_by_ids(
        self, db: AgnosticDatabase, ids: List[ObjectId]
    ) -> List[ModelType]:
        return await self.engine.find(self.model, self.model.id.in_(ids))

    async def get_multi(
        self,
        db: AgnosticDatabase,
        *,
        page: int = 0,
        limit: int = settings.MULTI_MAX,
        page_break: bool = False,
        **filters
    ) -> list[ModelType]:
        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": limit}
            if page_break
            else {}
        )

        query = self.build_eq_query(filters)
        return await self.engine.find(self.model, *query, **offset)

    async def create(
        self, db: AgnosticDatabase, *, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        return await self.engine.save(db_obj)

    async def update(
        self,
        db: AgnosticDatabase,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        await self.engine.save(db_obj)
        return db_obj

    async def remove(self, db: AgnosticDatabase, *, id: int) -> ModelType:
        obj = await self.model.get(id)
        if obj:
            await self.engine.delete(obj)
        return obj
