import strawberry

from .df import load_data
from .model import IrisModel

@strawberry.experimental.pydantic.type(
    model=IrisModel, 
    all_fields=True, 
    include_computed=True
)
class IrisType:
    pass
  
@strawberry.type
class IrisQuery:

    @strawberry.field
    def all_iris(self, n: int | None = None) -> list[IrisType]:
        df = load_data()
        if n is not None:
            df = df.sample(n, replace=True)

        records = [ 
            IrisModel.parse_obj(record)
            for record in df.to_dict(orient='records') 
        ] 
        return records
