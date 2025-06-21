
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor 
import time


app = FastAPI()
#uvicorn main:app --reload ------>to runserver

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
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



@app.get("/posts/")
def get_pots():
    cursor.execute("""SELECT * FROM posts """)
    my_posts = cursor.fetchall()
    return {"data": my_posts}


@app.post("/posts/", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data':new_post}

@app.get("/posts/{id}")
def get_post(id:str):
    cursor.execute("""SELECT * from posts where id = %s""",(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} not found')
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""Delete from posts where id = %s returning * """,(str(id),))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'post with id: {id} not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post : Post):
    cursor.execute("""UPDATE posts SET title = %s , content = %s, published = %s where id = %s returning *""",(post.title,post.content,post.published, id))
    update_post = cursor.fetchone()
    conn.commit()
    if update_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'post with id: {id} not found')

    return {'data':update_post}


