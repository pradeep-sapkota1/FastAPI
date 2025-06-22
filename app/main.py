
from fastapi import FastAPI, Response, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
#uvicorn main:app --reload ------>to runserver
# uvicorn app.main:app  --reload  , when i am in C:\Users\Pradeep\Documents\fastapi>



while True:
    try:
        conn = psycopg2.connect(host ='localhost',database='fastapi', user='postgres',password='9841102621',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DataBase Connection was Successful:")
        break
    except Exception as error:
        print("Connecting the database failed, The error was:")
        print(error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)