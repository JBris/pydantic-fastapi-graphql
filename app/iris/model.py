from pydantic import Field 
from .base import BaseModel

class IrisModel(BaseModel):
	variety: str = Field(
		default="Setosa",
		description="The flower variety",
	)
	
	sepal_length: float = Field(
		default=0,
		description="The flower sepal length",
		ge=0,
		unit="cm",
	)
	sepal_width: float = Field(
		default=0,
		description="The flower sepal width",
		ge=0,
		unit="cm",
	)
	petal_length: float = Field(
		default=0,
		description="The flower petal length",
		ge=0,
		unit="cm",
	)
	petal_width: float = Field(
		default=0,
		description="The flower petal width",
		ge=0,
		unit="cm",
	)