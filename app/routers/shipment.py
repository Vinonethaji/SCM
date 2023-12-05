
from fastapi import APIRouter, Request, Depends, HTTPException, Form, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi import Request, Depends, Form, HTTPException, status, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from jose import jwt
from bson import ObjectId
from datetime import datetime, timedelta
from jose import ExpiredSignatureError, JWTError
import re
from config.config import conn, Createshipment_collection
from app.routers.auth import decode_token, get_current_user_from_cookie, oauth2_scheme 
from app.routers.dashboard import check_authentication
import traceback


app = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@app.get("/myshipment", response_class=HTMLResponse, dependencies=[Depends(check_authentication)])
async def myshipment(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    try:
        if current_user is None or "username" not in current_user:
            return templates.TemplateResponse("signin.html", {"request": request, "error": "Not authenticated"})
        
        # Fetch shipment data from MongoDB based on the user's email
        shipment_data = list(Createshipment_collection.find({"email": current_user["email"]}))
        
        # Return the template with shipment data
        return templates.TemplateResponse("myshipment.html", {"request": request, "username": current_user["username"], "shipment_data": shipment_data})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    
@app.get("/password")
async def home_page(request: Request):
    return templates.TemplateResponse("password.html", {"request": request})

@app.get("/newpassword")
async def home_page(request: Request):
    return templates.TemplateResponse("newpassword.html", {"request": request})

# createshipment........

# New dependency function to check if the user is authenticated
async def check_authentication(current_user: dict = Depends(get_current_user_from_cookie)):
    if current_user is None:
       # Redirect unauthenticated user to the sign-in page
        redirect_url = "/signin"
        raise HTTPException(status_code=307, detail="Not authenticated", headers={"Location": redirect_url})
    return current_user


# existing route for the createshipment, now using the dependency
@app.get("/createshipment", response_class=HTMLResponse, dependencies=[Depends(check_authentication)])
async def createshipment(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    try:
        if current_user is None or "username" not in current_user:
            # Redirect unauthenticated user or user without username to the login page
            return templates.TemplateResponse("signin.html", {"request": request, "error": "Not authenticated"})

        # Continue rendering the createshipment for authenticated users
        return templates.TemplateResponse("createshipment.html", {"request": request, "username": current_user["username"]})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@app.post('/createshipment', response_model=dict)
def create_shipment(request: Request, shipment_number: str = Form(...),  
        route_details: str = Form(...),
        device: str = Form(...),
        po_number: str = Form(...),
        ndc_number: str = Form(...),
        serial_number: str = Form(...),
        container_number: str = Form(...),
        goods_type: str = Form(...),
        delivery_number: str = Form(...),
        pickup_date: str = Form(...),
        batch_id: str = Form(...),
        shipment_description: str = Form(...),
        current_user: dict = Depends(get_current_user_from_cookie)):
    try:
        # Ensure the user is authenticated
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Store the form data in MongoDB
        Createshipment_collection.insert_one({
            "email": current_user["email"],
            'ShipmentNumber': shipment_number,
            'RouteDetails': route_details,
            'Device': device,
            'PONumber': po_number,
            'NDCNumber': ndc_number,
            'SerialNumber': serial_number,
            'ContainerNumber': container_number,
            'GoodsType': goods_type,
            'DeliveryNumber': delivery_number,
            'PickupDate': pickup_date,
            'BatchId': batch_id,
            'ShipmentDescription': shipment_description
        })

        # Fetch updated shipment data from MongoDB based on the user's email
        shipment_data = list(Createshipment_collection.find({"email": current_user["email"]}))

        # Return a JSON response with the updated shipment data
        return JSONResponse(content={"ShipmentNumber": shipment_number, "RouteDetails": route_details, "Device": device,"PONumber": po_number,
                                       "NDCNumber": ndc_number, "SerialNumber": serial_number, "ContainerNumber": container_number, "GoodsType": goods_type, 
                                        "DeliveryNumber": delivery_number, "PickupDate": pickup_date, "BatchId": batch_id, "ShipmentDescription": shipment_description  })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
