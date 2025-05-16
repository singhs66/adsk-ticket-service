from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.daoLayer.database import engine, init_db
from app.v1.routers import tickets
from app.daoLayer.dataModel import ticketDO


ticketDO.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])


@app.on_event("startup")
def on_startup():
    init_db()
