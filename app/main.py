
from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from sqlalchemy.orm import Session

from app import models,schemas


from app.database import engine, get_db

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



@app.get("/posts/",response_model=List[schemas.Post])
def get_pots(db:Session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts """)
    #my_posts = cursor.fetchall()
    #return {"data": my_posts}
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts/", status_code= status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db)):
    #new_post = models.Post(title=post.title,content=post.content,published=post.published)
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


    #cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #return {'data':new_post}

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()

    #cursor.execute("""SELECT * from posts where id = %s""",(str(id),))
    #post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} not found')
    return post


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    #cursor.execute("""Delete from posts where id = %s returning * """,(str(id),))
    #delete_post = cursor.fetchone()
    #conn.commit()
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'post with id: {id} not found')
    
    post.delete(synchronize_session=False)  
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate,db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s , content = %s, published = %s where id = %s returning *""",(post.title,post.content,post.published, id))
    #update_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'post with id: {id} not found')

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
