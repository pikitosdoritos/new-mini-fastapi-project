from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    age: int

class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User

users = [
    {'id': 1, 'name': 'Nikita', 'age': 18}, 
    {'id': 2, 'name': 'Vasya', 'age': 28},
    {'id': 3, 'name': 'Berlond', 'age': 15}
]

posts = [
    {'id': 1, 'title': 'News 1', 'body': 'Text 1', 'author': users[1]},
    {'id': 2, 'title': 'News 2', 'body': 'Text 2', 'author': users[0]},
    {'id': 3, 'title': 'News 3', 'body': 'Text 3', 'author': users[2]}
]

# @app.get('/items')
# async def items() -> List[Post]:
#     post_obj = []
#     for post in posts:
#         post_obj.append(Post(id = post['id'], title = post['title'], body = post['body']))
#         return post_obj
    
@app.get('/items')
async def items() -> List[Post]:
   return [Post(**post) for post in posts]

@app.get('/items/{id}')
async def items(id: int) -> Post:
    for post in posts:
        if post['id'] == id:
            return Post(**post)
    raise HTTPException(status_code = 404, detail = 'Post not found')

@app.get('/search')
async def search(post_id: Optional[int] = None) -> Dict[str, Optional[Post]]:
    if post_id:
        for post in posts:
            if post['id'] == id:
                return {'data': Post(**post)}
        raise HTTPException(status_code = 404, detail = 'Post not found')
    else:
        return {'data': None}
    




# @app.get('/')
# async def homme() -> dict[str, str]:
#     return {'data': 'message'}

# @app.get('/contacts')
# async def contacts() -> int:
#     return 34