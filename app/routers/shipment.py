
from fastapi import APIRouter, Request, Depends, HTTPException, Form, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi import Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from config.config import client, shipment_collection
from app.routers.auth import decode_token, get_current_user_from_cookie
from app.routers.dashboard import check_authentication



app = APIRouter()
templates = Jinja2Templates(directory="templates")


# ........................myshipment.............................

@app.get("/myshipment", response_class=HTMLResponse, dependencies=[Depends(check_authentication)])
async def myshipment(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    try:
        if current_user is None or "username" not in current_user:
            return templates.TemplateResponse("signin.html", {"request": request, "error": "Not authenticated"})
        
        # Fetch shipment data from MongoDB based on the user's email
        shipment_data = list(shipment_collection.find({"email": current_user["email"]}))
        
        # Return the template with shipment data
        return templates.TemplateResponse("myshipment.html", {"request": request, "username": current_user["username"], "shipment_data": shipment_data})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



# ..........................createshipment.............................

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
        expected_delivery: str = Form(...),
        batch_id: str = Form(...),
        shipment_description: str = Form(...),
        
        current_user: dict = Depends(get_current_user_from_cookie)):
    try:
        # Ensure the user is authenticated
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        
       # Update the server-side Python code to return an error message
        if len(shipment_number) < 7 or not shipment_number.isdigit():
            return templates.TemplateResponse("createshipment.html", {"request": request, "shipment_number_error": "Shipment number must be a 7-digit number"})

        # Check if the shipment is already registered
        existing_shipment =shipment_collection.find_one({"ShipmentNumber": shipment_number})

        if existing_shipment:
            # raise HTTPException(status_code=400, detail="Shipment already exists")
            return templates.TemplateResponse("createshipment.html", {"request": request, "shipment_number_error": "Shipment already exists"})

        # Store the form data in MongoDB
        shipment_collection.insert_one({
            "username": current_user["username"],
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
            'ExpectedDeliveryDate': expected_delivery,
            'BatchId': batch_id,
            'ShipmentDescription': shipment_description
        })

        # Fetch updated shipment data from MongoDB based on the user's email
        shipment_data = list(shipment_collection.find({"email": current_user["email"]}))

        return templates.TemplateResponse("myshipment.html", {"request": request, "shipment_data": shipment_data})
      

    except Exception as e:
        return templates.TemplateResponse("createshipment.html", {"request": request, "error_message": f"Internal Server Error: {str(e)}"})
