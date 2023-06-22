import pytest
from fastapi.testclient import TestClient
from database.database import SessionLocal, engine
from database.models import Base, Post
from main import app

client = TestClient(app)


# Test veritabanını oluşturmak için kullanılacak pytest fixture'ı
@pytest.fixture
def test_db():
    # Test veritabanını oluştur
    Base.metadata.create_all(bind=engine)

    # Test veritabanına bazı örnek veriler ekleyelim
    with SessionLocal() as db:
        # Örnek gönderi verileri
        posts_data = [
            {
                'title': 'Post 1',
                'content': 'Content 1',
                'author': 'Author 1',
                'upvotes': 10,
            },
            {
                'title': 'Post 2',
                'content': 'Content 2',
                'author': 'Author 2',
                'upvotes': 20,
            },
            {
                'title': 'Post 3',
                'content': 'Content 3',
                'author': 'Author 3',
                'upvotes': 30,
            },
        ]

        # Örnek gönderileri test veritabanına ekle
        for post in posts_data:
            db_post = Post(**post)
            db.add(db_post)
        db.commit()

    yield

    # Testler tamamlandıktan sonra veritabanını temizle
    Base.metadata.drop_all(bind=engine)


def test_get_posts(test_db):
    response = client.get('/posts')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert (
        len(response.json()) >= 3
    )  # Test veritabanında 3 veya daha fazla gönderi olduğunu doğrula


def test_get_post(test_db):
    # Örnek bir post_id değeri
    post_id = 1
    response = client.get(f'/posts/{post_id}')
    assert response.status_code == 200
    assert response.json().get('id') == post_id


def test_delete_post(test_db):
    # Örnek bir post_id değeri
    post_id = 1
    response = client.delete(f'/posts/{post_id}')
    assert response.status_code == 200
    assert response.json().get('message') == 'Post deleted successfully'
