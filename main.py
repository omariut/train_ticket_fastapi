from fastapi import FastAPI
from routers import admin, public
from fastapi import APIRouter
app = FastAPI()
routers = APIRouter()
routers.include_router(admin.station_router)
routers.include_router(admin.train_router)
routers.include_router(admin.cart_router)
routers.include_router(admin.coach_router)
routers.include_router(admin.seat_router)
routers.include_router(public.ticket_router)
app.include_router(routers)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}