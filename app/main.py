from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os
import os.path as osp
from pymongo import MongoClient
from sqlmodel import create_engine, Session, SQLModel, select
import strawberry
from strawberry.fastapi import GraphQLRouter
from iris import IrisModel, IrisSQL, load_data, IrisRepository, IrisDocument, IrisDataFrame, IrisQuery, IrisFactory

load_dotenv(osp.join("..", ".env"))

sql_creds = os.getenv("DB_CONNECTION", "postgresql://user:password@localhost:5432/pydantic")
engine = create_engine(sql_creds)
SQLModel.metadata.create_all(engine)

mongo_creds = os.getenv("MONGO_CONNECTION", "mongodb://user:password@localhost:27017")
client = MongoClient(mongo_creds)
database = client["pydantic"]
repo = IrisRepository(database)

schema = strawberry.Schema(query=IrisQuery)
graphql_app = GraphQLRouter(schema)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.get("/df")
async def get_df():
    df = load_data()
    records = df.to_dict(orient='records')
    return records

@app.get("/validate-df")
async def validate_df():
    df = load_data()
    validated_df = IrisDataFrame.validate(df)
    records = validated_df.to_dict(orient='records')
    return records

@app.get("/mock")
async def mock_model() -> IrisModel:
    mock_object = IrisFactory.build()
    return mock_object

@app.get("/mock-copula")
async def mock_copula() -> list[IrisModel]:
    mock_objects = IrisFactory.from_copula()
    return mock_objects

@app.get("/mongo")
async def get_mongo() -> list[IrisDocument]:    
    return repo.find_by({})

@app.post("/mongo")
async def post_mongo() -> list[IrisDocument]:       
    df = load_data()
    records = [ 
        IrisDocument.parse_obj(record)
        for record in df.to_dict(orient='records') 
    ] 
    repo.save_many(records)
    return records

@app.get("/sql")
async def get_sql() -> list[IrisSQL]:       
    df = load_data()
    records = [ 
        IrisSQL.parse_obj(record)
        for record in df.to_dict(orient='records') 
    ] 

    with Session(engine) as session:
        records = session.exec(select(IrisSQL)).all()
        
    return records

@app.post("/sql")
async def post_sql() -> list[IrisSQL]:       
    df = load_data()
    records = [ 
        IrisSQL.parse_obj(record)
        for record in df.to_dict(orient='records') 
    ] 
    
    with Session(engine) as session:
        session.add_all(records)
        session.commit()
        for record in records:
            session.refresh(record)
    return records

app.include_router(graphql_app, prefix="/graphql")
app.add_websocket_route("/graphql", graphql_app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)