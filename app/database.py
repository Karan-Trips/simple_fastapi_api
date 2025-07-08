from sqlmodel import  SQLModel, Session, create_engine

# DATABASE_URL = "mysql+pymysql://root@localhost:3306/fastapi_demo" //FOR MYSQL DATABASE

DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost:5432/fastapi"

engine = create_engine(DATABASE_URL, echo=False,)


def get_db():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)