from sqlmodel import  SQLModel, Session, create_engine

# DATABASE_URL = "mysql+pymysql://root@localhost:3306/fastapi_demo" //FOR MYSQL DATABASE

DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost:5432/fastapi" #//Local database PostGres
# DATABASE_URL = "postgresql+psycopg2://karan:CMHqmcidIiRvru418E19bd3h89yaE6tG@dpg-d1mgrhidbo4c73fa368g-a.oregon-postgres.render.com/fastapi_h657" 


engine = create_engine(DATABASE_URL, echo=False,)


def get_db():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)