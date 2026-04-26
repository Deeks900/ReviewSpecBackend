from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Spec Reviewer API")

app.include_router(router)