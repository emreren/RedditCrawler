import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from database.database import SessionLocal, engine
from database.models import Base, Post

async def login_and_scrape():

    # Veritabanı bağlantısı ve oturumu oluşturma
    session = SessionLocal()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()

        # Burada giriş yapma işlemini gerçekleştirin (kullanıcı adı ve şifrenizi girin)               
        await page.goto("https://www.reddit.com/login")
        await page.fill('input[name="username"]', username)
        await page.fill('input[name="password"]', password)
        await page.click('button[type="submit"]')        
        try:
            await page.wait_for_load_state('networkidle', timeout=60000)
        except:
            pass        
        
        # Giriş yapıldıktan sonra hedef subreddit sayfasına gidin
        await page.goto(f'https://reddit.com/r/{subreddit_name}/new',timeout=60000)
        await page.keyboard.press('End')
        await page.wait_for_timeout(30000)

        # Sayfanın içeriğini alın   
        page_content= await page.content()
        await browser.close()

        # BeautifulSoup kullanarak postları yakalayın
        soup = BeautifulSoup(page_content, 'html.parser')
        post_elements = soup.select('.Post')
        for post in post_elements:
            title_element = post.select_one('div[data-adclicklocation="title"] h3')
            title = title_element.get_text() if title_element else ''

            # Extracting the content
            content_element = post.select_one('div[data-adclicklocation="background"]')
            content = content_element.get_text(strip=True) if content_element else ''

            # Extracting the upvotes
            upvote_element = post.select_one('div[data-adclicklocation="background"] button[data-click-id="upvote"]')
            upvotes = upvote_element.find_next_sibling('div').get_text() if upvote_element else '0'
            if upvotes == "Vote":
                upvotes="0"
            # Extracting the author
            author_element = post.select_one('a[data-testid="post_author_link"]')
            author = author_element.get_text() if author_element else ''

            if session.query(Post).filter(Post.title == title).first():
                continue
            post = Post(title=title, content=content, author=author, upvotes=upvotes)
            session.add(post)

            print('Title:', title)
            print('Content:', content)
            print('Upvotes:', upvotes)
            print('Author:', author)

        session.commit()
        session.close()         
        


# Kullanıcı adı, şifre, subreddit'i ve veritabanı dosyası adını ayarlayın
username = "CHANGE_ME"
password = "CHANGE_ME"
subreddit_name = "cybersecurity"












