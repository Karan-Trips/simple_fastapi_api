from piccolo.engine.postgres import PostgresEngine

DB = PostgresEngine(
    config={
        "database": "fastapi",
        "user": "postgres",
        "password": "123",
        "host": "localhost",
        "port": 5432,
    }
)

APP_REGISTRY = [
    "piccolo.apps.user.piccolo_app",
    "piccolo_admin.piccolo_app",
] 