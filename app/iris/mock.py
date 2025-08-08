from polyfactory.factories.pydantic_factory import ModelFactory
from faker import Faker
import random 
from sklearn.preprocessing import LabelEncoder
from copulas.multivariate import GaussianMultivariate

from .df import load_data
from .model import IrisModel

class IrisFactory(ModelFactory[IrisModel]):
    __model__ = IrisModel
    __random_seed__ = 1
    __faker__ = Faker(locale="en_NZ")

    @classmethod
    def variety(cls) -> str:
        return random.choice(["Setosa", "Virginica", "Versicolor"])
    
    @classmethod
    def from_copula(cls) -> list[IrisModel]:
        df = load_data()
        encoder = LabelEncoder()
        df['variety'] = encoder.fit_transform(df['variety'])
        copula = GaussianMultivariate()
        copula.fit(df)

        mock_df = copula.sample(len(df))
        mock_df["variety"] = mock_df['variety'].astype("int")
        mock_df["variety"] = encoder.inverse_transform(mock_df["variety"])
        num_cols = mock_df.select_dtypes(include='number').columns
        mock_df[num_cols] = mock_df[num_cols].clip(lower=0)

        records = [ 
            IrisModel.parse_obj(record)
            for record in mock_df.to_dict(orient='records') 
        ] 
        return records