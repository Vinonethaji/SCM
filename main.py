from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles 
from app.routers.user import app as user  # Import the user routers from app routes
from app.routers.shipment import app as shipment
from app.routers.dashboard import app as dashboard
from app.routers.datastream import app as datastream






app = FastAPI()


app.include_router(user)
app.include_router(shipment)
app.include_router(dashboard)
app.include_router(datastream)

# app.include_router(datastream)

# app.include_router(trial.app)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

