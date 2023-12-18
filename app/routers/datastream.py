from fastapi import APIRouter, HTTPException, Depends, status
from fastapi import Request, Depends, Form, HTTPException, status, Cookie
from fastapi.responses import HTMLResponse
from app.routers.dashboard import check_authentication
from config.config import client, device_collection 
from app.routers.auth import get_current_user_from_cookie
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = APIRouter()

templates = Jinja2Templates(directory="templates")
template_path = Path("templates").resolve()


# .....................datastream........................

@app.get("/datastream", response_class=HTMLResponse, dependencies=[Depends(check_authentication)])
async def datastream(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    try:
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
                
      
        role = current_user.get('role')
      
        if role != "admin":
            return templates.TemplateResponse("unauthorized.html", {"request": request})

        return templates.TemplateResponse("datastream.html", {"request": request})
    except HTTPException as e:
        print(f"HTTPException: {e}")
        raise e
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {str(e)}")


@app.post("/datastream", response_class=HTMLResponse)
async def datastream(request: Request, current_user: dict = Depends(get_current_user_from_cookie),
                    deviceid: int = Form(...)):
    try:
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

        role = current_user.get('role')

        if role != "admin":
            error_message = f"Sorry {current_user.get('username')}, you are allowed to access this page"
            return templates.TemplateResponse("dashboard.html", {"request": request, "error_message": error_message})

         # Fetch device data from the MongoDB collection based on the selected device ID
        device_data_cursor = device_collection.find({"Device_ID": deviceid}, {"_id": 0})
        device_data = list(device_data_cursor)  # Convert cursor to list
        print(f"Device ID: {deviceid}")
        print(f"Device Data: {device_data}")

        return templates.TemplateResponse("datastream.html", {"request": request, "device_data": device_data})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")
    


# .......................unauthorized.......................    

@app.get("/unauthorized", response_class=HTMLResponse, dependencies=[Depends(check_authentication)])
async def unauthorized(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    try:
        if current_user is None or "username" not in current_user:
            # Redirect unauthenticated user or user without username to the login page
            return templates.TemplateResponse("signin.html", {"request": request, "error": "Not authenticated"})

        # Continue rendering the unauthorized for authenticated users
        return templates.TemplateResponse("unauthorized.html", {"request": request, "username": current_user["username"]})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")
    