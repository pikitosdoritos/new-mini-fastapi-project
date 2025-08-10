from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from models import Base, User, Post
from database import engine, session_local
from schemas import UserCreate, PostCreate, PostResponse, User as DbUser

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://192.168.1.13:8080", # Добавляем и IP-адрес на всякий случай
]

# 3. Добавляем middleware в приложение
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Разрешаем источники из списка
    allow_credentials=True, # Разрешаем куки
    allow_methods=["*"],    # Разрешаем все методы (GET, POST, etc.)
    allow_headers=["*"],    # Разрешаем все заголовки
)

Base.metadata.create_all(bind = engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.post('/users/', response_model = DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = User(name = user.name, age = user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post('/posts/', response_model = PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> Post:
    db_user = db.query(User).filter(User.id == post.author_id).first()

    if db_user is None:
        raise HTTPException(status_code = 404, detail = 'User not found')

    db_post = Post(title = post.title, body = post.body, author_id = post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post

@app.get('/posts/', response_model = List[PostResponse])
async def posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

@app.get('/users/{name}', response_model = DbUser)
async def get_user_by_name(name: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == name).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user 