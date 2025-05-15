from fastapi import FastAPI
from app.v1.routers import tickets

app = FastAPI()
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
