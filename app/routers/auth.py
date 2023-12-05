from passlib.context import CryptContext
from jose import jwt, ExpiredSignatureError, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Request, Depends, HTTPException, Form, Cookie, status
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import os
from dotenv import load_dotenv
from config.config import signup_collection
import secrets

app = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# Load environment variables from a .env file
load_dotenv()

# Create an instance of CryptContext for password hashing and verification
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    def hash_password(pwd: str):   #hashing the password
        return pwd_cxt.hash(pwd)

    def verify_password(pwd: str, hashed_password: str):  #verify the hashed password
        return pwd_cxt.verify(pwd, hashed_password)

# Load environment variables for JWT configuration
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES  = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")



# OAuth2PasswordBearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


###### ----------function to create access token(JWT) for user authenication----------######

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()     # Make a copy of the input data dictionary
    # Calculate the token expiration time
    if expires_delta: 
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



###### ----------function decode the JWT token----------######

def decode_token(token: str):
    try:
        # Attempt to decode the provided token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})



###### ----------function to get current user from access token----------######

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload



###### ----------function to get current user from access token stored in the cookies----------######
async def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if token is None:
        return None

    try:
        payload = decode_token(token)
        if payload and "sub" in payload and "email" in payload:
            user_data = signup_collection.find_one({"email": payload["email"]})
            if user_data and "username" in user_data:
                return {"username": user_data["username"], "email": payload["email"], "role": user_data.get("role")}
    except JWTError:
        pass

    return None


# Function to clear the access token cookie
def clear_access_token_cookie(response: RedirectResponse):
    print("Clearing access token cookie") 
    # Set the access token cookie to an expired value
    response.delete_cookie(key="access_token")

