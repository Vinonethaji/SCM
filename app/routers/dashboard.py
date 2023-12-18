
from fastapi import APIRouter, Request, Depends, HTTPException, Form, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi import Request, Depends, Form, HTTPException, Cookie
from fastapi.responses import HTMLResponse
from config.config import client, user_collection
from app.routers.auth import  get_current_user_from_cookie


app = APIRouter()
templates = Jinja2Templates(directory="templates")


# New dependency function to check if the user is authenticated
async def check_authentication(current_user: dict = Depends(get_current_user_from_cookie)):
    if current_user is None:
       # Redirect unauthenticated user to the sign-in page
        redirect_url = "/signin"
        raise HTTPException(status_code=307, detail="Not authenticated", headers={"Location": redirect_url})
    return current_user


# ................ dashboard.......................
@app.get("/dashboard", response_class=HTMLResponse, dependencies=[Depends(check_authentication)])
async def dashboard(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    try:
        if current_user is None or "username" not in current_user:
            # Redirect unauthenticated user or user without username to the login page
            return templates.TemplateResponse("signin.html", {"request": request, "error": "Not authenticated"})

        # Continue rendering the dashboard for authenticated users
        return templates.TemplateResponse("dashboard.html", {"request": request, "username": current_user["username"]})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")
    
#........... myaccount...........
@app.get("/my_account", response_class=HTMLResponse, dependencies=[Depends(check_authentication)])
async def my_account(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    try:
        if current_user is None or "username" not in current_user:
            # Redirect unauthenticated user or user without username to the login page
            return templates.TemplateResponse("signin.html", {"request": request, "error": "Not authenticated"})

        # Fetch user data from MongoDB based on the user's email
        user_data = user_collection.find_one({"email": current_user["email"]})

        # Continue rendering the my_account page for authenticated users
        return templates.TemplateResponse("my_account.html", {"request": request, "username": current_user["username"], "email": current_user["email"], "role": current_user.get("role")})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")