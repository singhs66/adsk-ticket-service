from fastapi import FastAPI, status
from app.auth.routes import router as auth_router
from app.daoLayer.database import engine, init_db
from app.v1.routers import tickets
from app.daoLayer.dataModel import ticketDO
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from app.cacheRedis import RedisCache

# Load environment variables from .env file for local development
load_dotenv()

ticketDO.Base.metadata.create_all(bind=engine)

app = FastAPI()

# This is added for making it work the ui locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"] for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "ok"}


@app.get("/redis-health")
def redis_health():
    if RedisCache.ping():
        return {"status": "ok"}
    else:
        return {"status": "error"}, 500
