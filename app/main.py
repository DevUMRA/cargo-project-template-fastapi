from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.auth.router import router as auth_router
from app.db.session import engine

app = FastAPI(
    title="Cargo Platform API",
    description="FastAPI негізіндегі карго платформасы",
    version="1.0.0"
)

app.include_router(auth_router)



@app.get("/")
def home():
    return {"message": "Cargo API is running"}

@app.get("/hello")
def hello_world():
    return {"message": "Hello World"}


@app.get("/health", tags=["health"])
def health():
    """Docker / Qoldanba healthcheck: қолданба тірі және дерекқорға қосыла алады."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(status_code=503, content={"status": "error", "database": "unavailable"})
    return {"status": "ok", "database": "ok"}