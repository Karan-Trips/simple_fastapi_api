from uu import decode
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from app import models, database
from app.connection_manager import ConnectionManager
from app.router import user_api as user, todo_api as todo
from sqladmin import Admin, ModelView
from sqlmodel import SQLModel, Session, select
from app.auth_token_genration import decode_token, get_current_user
from jose import JWTError

models.SQLModel.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(user.user_router)
app.include_router(todo.todo_router)

# SQLAdmin setup
class UserAdmin(ModelView, model=models.User):
    column_list = ["id", "name", "email", "token"]
    form_columns = ["name", "email", "password", "token"]  # All editable fields
    column_searchable_list = ["name", "email"]
    name = "User"
    name_plural = "Users"

class TodoAdmin(ModelView, model=models.Todo):
    column_list = ["id", "task", "status", "user"]
    form_columns = ["task", "status", "user_id"]  # All editable fields
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
manager = ConnectionManager()
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    try:
        user = decode_token(token)  
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(token, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(token, f"{user['username']}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(token, websocket)


@app.get("/", tags=["root"])
async def root():
    return {"message": "API Started Successfully"}
