from fastapi import FastAPI
from app import models, database
from app.router import user_api as user, todo_api as todo
from sqladmin import Admin, ModelView
from sqlmodel import SQLModel, Session, select

models.SQLModel.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(user.user_router)
app.include_router(todo.todo_router)

class UserAdmin(ModelView, model=models.User):
    column_list = ["id", "name", "email", "token"]
    form_columns = ["name", "email", "password", "token"]
    column_searchable_list = ["name", "email"]
    name = "User"
    name_plural = "Users"

class TodoAdmin(ModelView, model=models.Todo):
    column_list = ["id", "task", "status", "user"]
    form_columns = ["task", "status", "user_id"]
    column_searchable_list = ["task"]
    name = "Todo"
    name_plural = "Todos"

    async def get_form_choices(self, request, obj=None):
        with Session(database.engine) as session:
            users = session.exec(select(models.User)).all()
        return {
            "user_id": [(user.id, f"{user.name} ({user.email})") for user in users]
        }

admin = Admin(app, database.engine)
admin.add_view(UserAdmin)
admin.add_view(TodoAdmin)

@app.get("/", tags=["root"])
async def root():
    return {"message": "API Started Successfully"}
