from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles 
from app.routers.user import app as user 
from app.routers.shipment import app as shipment
from app.routers.dashboard import app as dashboard
from app.routers.datastream import app as datastream
from app.routers.password import app as password






app = FastAPI()


app.include_router(user)
app.include_router(shipment)
app.include_router(dashboard)
app.include_router(datastream)
app.include_router(password)


app.mount("/static", StaticFiles(directory="static"), name="static")

