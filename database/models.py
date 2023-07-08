from sqlalchemy import Column, Integer, String

from database.database import Base, engine



class Post(Base):
    """Veritabanında kullanılacak olan Post modelini tanımlar."""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    content = Column(String, nullable=True)
    author = Column(String)
    upvotes = Column(String)

    def __repr__(self):
        return f'<Post {self.id}>'


Base.metadata.create_all(bind=engine)
