from piccolo_admin.endpoints import create_admin
from starlette.applications import Starlette

admin_app = create_admin(
    tables=[], 
    site_name="My FastAPI Admin"
)

def get_admin_app():
    return admin_app 