import praw

from database.database import SessionLocal
from database.models import Post

# Reddit API istemci kimlik bilgilerini girin
client_id = 'CHANGE ME'
client_secret = 'CHANGE ME'
user_agent = 'CHANGE ME'

# PRAW istemcisini oluşturun
reddit = praw.Reddit(
    client_id=client_id, client_secret=client_secret, user_agent=user_agent,
)

# Crawl edilecek subreddit ve post sayısı
subreddit_name = 'cybersecurity'
post_count = 100

# Subreddit'i alın
subreddit = reddit.subreddit(subreddit_name)


def get_latest_posts():
    try:
        # Belirtilen sayıda en son postları alın
        new_posts = subreddit.new(limit=post_count)

        with SessionLocal() as db:
            for post in new_posts:
                if db.query(Post).filter(Post.title == post.title).first():
                    continue
                db_post = Post(
                    content=post.selftext,
                    title=post.title,
                    author=post.author.name,
                    upvotes=post.score,
                )
                db.add(db_post)
            db.commit()
    except Exception as error:
        print('Error: ', error)
