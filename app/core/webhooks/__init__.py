from fastapi import FastAPI
from core.webhooks import handlers


app = FastAPI()
app.include_router(handlers.router)
