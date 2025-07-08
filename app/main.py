from fastapi import FastAPI
from app import models, database
from app.router import user_api as user, todo_api as todo
from app import models, database

models.SQLModel.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(user.user_router)
app.include_router(todo.todo_router)


@app.get("/", tags=["root"])
async def root():
    return {"message": "API Started Successfully"}
