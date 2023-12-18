
from fastapi import APIRouter, Request, Depends, HTTPException, Form, Cookie, requests
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from app.routers.user import validate_password
from config.config import client, user_collection  
from app.routers.auth import  pwd_cxt
import os

app = APIRouter()
templates = Jinja2Templates(directory="templates")




###### ----------Route for reset password----------######
  
@app.get("/newpassword")
async def newpassword(request: Request):
    return templates.TemplateResponse("newpassword.html", {"request": request})


@app.post("/newpassword", response_class=JSONResponse)
async def reset_password(request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirmpassword: str = Form(...),
):
    try:

        user = user_collection.find_one({'email': email})
        # Check if passwords match
        if password != confirmpassword:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        # Check if passwords match
        validate_password(password, confirmpassword)

        # Hash the new password
        hashed_password = pwd_cxt.hash(password)

        # Update the user's password in the database
        result = user_collection.update_one(
            {"email": email},
            {"$set": {"password": hashed_password}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

       
         # Render the newpassword.html template with the success message
        response = templates.TemplateResponse("newpassword.html", {"request": request, "message": "Password reset successfully, Redirecting to signin page"})

        # Return the response with the success message
        return response
    
    
    except HTTPException as e:
        # Render the signup template with the error message
        return templates.TemplateResponse("newpassword.html", {"request": request, "error_message": str(e)})

    

