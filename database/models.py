from sqlalchemy import Column, Integer, String, DateTime

from database.database import Base, engine


class Post(Base):
    """Veritabanında kullanılacak olan Post modelini tanımlar."""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time = Column(DateTime)
    upvotes = Column(String)
    author = Column(String)
    title = Column(String)
    content = Column(String, nullable=True)


    def __repr__(self):
        return f'<Post {self.id}>'


Base.metadata.create_all(bind=engine)
