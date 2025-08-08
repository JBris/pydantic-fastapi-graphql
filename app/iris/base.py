from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
	class Config:
		arbitrary_types_allowed = True
		protected_namespaces = ()
		# from_attributes = True