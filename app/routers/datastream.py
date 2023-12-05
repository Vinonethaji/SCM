from datetime import datetime, timedelta
from typing import Annotated
from typing import Optional, Dict
from fastapi import Depends,APIRouter, FastAPI, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

app = APIRouter()
templates = Jinja2Templates(directory="app/templates")



@app.get("/datastream")
async def home_page(request: Request):
    return templates.TemplateResponse("datastream.html", {"request": request})