import pandera.pandas as pa
from pandera.engines.pandas_engine import PydanticModel
from .model import IrisModel
import os.path as osp
import pandas as pd

def load_data(infile: str | None = None) -> pd.DataFrame:
    if infile is None:
        infile = osp.join("data", "iris.csv")
        
    df = pd.read_csv(infile)
    return df

class IrisDataFrame(pa.DataFrameModel):
    class Config:
        dtype = PydanticModel(IrisModel)
        coerce = True 
