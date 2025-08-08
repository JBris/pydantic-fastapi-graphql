
from sqlmodel import SQLModel, Field
from pydantic_mongo import AbstractRepository, PydanticObjectId
from .model import IrisModel

class IrisSQL(IrisModel, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

class IrisDocument(IrisModel):
    id: PydanticObjectId | None = Field(default=None)

class IrisRepository(AbstractRepository[IrisDocument]):
   class Meta:
      collection_name = 'iris'
