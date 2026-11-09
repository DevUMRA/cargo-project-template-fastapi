from fastapi import FastAPI
from app.auth.router import router as auth_router

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