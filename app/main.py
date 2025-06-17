from random import randrange
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor 


app = FastAPI()
#uvcorn main:app --reload to runserver

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

try:
    conn = psycopg2.connect(host ='localhost',database='fastapi', user='postgres',password='9841102621',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("DataBase Connection was Successful")
except Exception as error:
    print("Connecting the datapase failed with error:")
    print(error)

my_posts = [{"title":"title of post 1","content":"content of post 1", "id":1},{"title":"title of post 2","content":"content of post 2", "id":2}]


def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            print(p)
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/posts/")
def get_pots():
    return {"data": my_posts}


@app.post("/posts/", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {'data': my_posts}

@app.get("/posts/{id}")
def get_post(id:int, response : Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message':f'post with id: {id} not found'}
    print(id)
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    print("adkfjdlfkjdlfjlfjd", flush=True)
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found')
    print(index)
    my_posts.pop(index)
    return{'message':f'post of id: {id} is deleted'}

    # deleting post
    # find the index in the array that is required ID
    # my_posts.pop(index)
@app.put("/posts/{id}")
def update_post(id: int, post : Post):
    index = find_index_post(id)
    if index== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} not found')
    post_dict = post.dict()
    post_dict["id"]= id
    my_posts[index] = post_dict
    print(my_posts)
    return {'message':'updated post'}


