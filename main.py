from fastapi import FastAPI
from sqlalchemy.orm import Session

from crawler import get_latest_posts
from database.database import SessionLocal
from database.models import Post

app = FastAPI()


# veritabanından tüm gönderileri alır ve döndürür.
@app.get('/posts')
async def get_posts():
    get_latest_posts()
    with SessionLocal() as db:
        return db.query(Post).all()


# belirli bir post_id'ye sahip gönderiyi veritabanından bulur ve döndürür.
@app.get('/posts/{post_id}')
async def get_post(post_id: int):
    db: Session = SessionLocal()
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return {'message': 'Post not found'}
    return post

# belirli bir post_id'ye sahip gönderiyi veritabanından bulur ve siler.
@app.delete('/posts/{post_id}')
async def delete_post(post_id: int):
    with SessionLocal() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return {'message': 'Post not found'}
        db.delete(post)
        db.commit()
        return {'message': 'Post deleted successfully'}
