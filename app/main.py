from fastapi import FastAPI
from app.routes.user import user

app = FastAPI()
app.include_router(user)
