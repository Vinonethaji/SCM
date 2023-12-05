
from fastapi import APIRouter, Request, Depends, HTTPException, Form, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi import Request

from fastapi.responses import HTMLResponse, RedirectResponse
from jose import jwt
from bson import ObjectId
from datetime import datetime, timedelta
import re
from config.config import conn, signup_collection  
from app.routers.auth import Hash, create_access_token, clear_access_token_cookie

import os

app = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def validate_password(password, confirm_password):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Validate password requirements
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    if not any(char.isupper() for char in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")

    if not any(char.isdigit() for char in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one digit")

    special_characters = set("!@#$%^&*(),.?\":{}|<>-_+=")
    if not any(char in special_characters for char in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character")

    return None

# homepage..............
@app.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

# signup.........................
@app.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})
from fastapi import HTTPException

@app.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), confirmpassword: str = Form(...)):
    print("Received POST request to /signup") 
    try:
        # Check if the username already exists
        existing_user = signup_collection.find_one({"email": email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered!")

        # Check if passwords match
        validate_password(password, confirmpassword)

        # Hash the password
        hashed_password = Hash.hash_password(password)

        # Create a new user document
        new_user = {
            "username": username,
            "password": hashed_password,
            "email": email,
            "role": "User"
        }

        # Insert the new user into the MongoDB collection
        signup_collection.insert_one(new_user)
        print(new_user)

        # Create a RedirectResponse to the sign-in page with success message
        redirect_url = '/signin'
        return RedirectResponse(url=redirect_url, status_code=302)

    except HTTPException as e:
        # Render the signup template with the error message
        return templates.TemplateResponse("signup.html", {"request": request, "error_message": str(e)})

# signin.....................
@app.get("/signin")
async def signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.post("/signin", response_class=HTMLResponse)
async def signin(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = signup_collection.find_one({"email": form_data.username})

        if user is None:
            # Render the login page with an error message
            return templates.TemplateResponse("signin.html", {"request": request, "error_message": {"message": "User not found!", "class": "error-message"}})


        if not Hash.verify_password(form_data.password, user["password"]):
            # Render the login page with an error message
            return templates.TemplateResponse("signin.html", {"request": request, "error_message": {"message": "Incorrect Password!", "class": "error-message"}})

        current_user = {
            "username": user["username"],
            "email": user["email"]
        }

        access_token = create_access_token(
            data={"sub": user["username"], "email": user["email"]})
        print(access_token)

        response = RedirectResponse("/dashboard", status_code=302)
        response.set_cookie(key="access_token", value=access_token, httponly=True)

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@app.get("/favicon.ico")
async def favicon():
    return


@app.post("/forgot-password")
def forgot_password(email: str):
    # Check if the email exists in the database
    user = signup_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate a reset token
    reset_token = jwt.encode(
        {"user_id": str(user["_id"]), "exp": datetime.utcnow() + timedelta(minutes=30)},
        os.getenv("SECRET_KEY"),
        algorithm="HS256"
    )

    # Send the reset token to the user's email (implementation not included)

    return {"message": "Reset token sent to your email"}

@app.get("/reset-password")
def reset_password(token: str):
    try:
        # Verify the reset token
        decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        user_id = decoded_token["user_id"]
        user = signup_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Render the password reset page with the token
        return templates.TemplateResponse("reset_password.html", {"request": Request, "token": token})
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")  



# Your existing route for logout
@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request, access_token: str = Cookie(None)):
    print("Logout route triggered")
    try:
        # Clear the access token cookie to log the user out
        response = RedirectResponse(url="/")
        # Call the function to clear the access token cookie
        clear_access_token_cookie(response)
        return response  # Return the RedirectResponse
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")
