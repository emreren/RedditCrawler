from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite veritabanı bağlantısı ve oturumu oluşturma
DATABASE_URL = 'sqlite:///reddit_posts.db'
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Test veritabanı için
test_engine = create_engine('sqlite:///:memory:', echo=True)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
