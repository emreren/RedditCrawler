from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from database.database import SessionLocal
from database.models import Post

# Kullanıcı adı, şifre, subreddit'i ve veritabanı dosyası adını ayarlayın
username = "CHANGE_ME"
password = "CHANGE_ME"
subreddit_name = "cybersecurity"

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
            await page.wait_for_load_state('load', timeout=60000)
        except:
            pass

        # Giriş yapıldıktan sonra hedef subreddit sayfasına gidin
        await page.goto(f'https://reddit.com/r/{subreddit_name}/new', timeout=60000)
        await page.keyboard.press('End')
        await page.wait_for_load_state('load', timeout=60000)

        # Sayfanın içeriğini alın   
        page_content = await page.content()
        await browser.close()

        # BeautifulSoup kullanarak postları yakalayın
        soup = BeautifulSoup(page_content, 'html.parser')
        post_elements = soup.select('.Post')
        for post in post_elements:
            title_element = post.select_one('div[data-adclicklocation="title"] h3')
            title = title_element.get_text() if title_element else ''

            # content yakalama
            content_element = post.select_one('div[data-click-id="text"]')
            content = content_element.get_text(separator="\n") if content_element else ""

            # upvotes yakalama
            upvote_element = post.select_one('div[data-adclicklocation="background"] button[data-click-id="upvote"]')
            upvotes = upvote_element.find_next_sibling('div').get_text() if upvote_element else '0'
            if upvotes == "Vote":
                upvotes = "0"

            # author yakalama
            author_element = post.select_one('a[data-testid="post_author_link"]')
            author = author_element.get_text() if author_element else ''

            # time yakalama
            post_timestamp_element = post.select_one('span[data-testid="post_timestamp"]')
            post_timestamp = post_timestamp_element.get_text(strip=True) if post_timestamp_element else ''

            # veritabanına ekleme
            if session.query(Post).filter(Post.title == title).first():
                continue
            post = Post(title=title, content=content, author=author, upvotes=upvotes, time=post_timestamp)
            session.add(post)

            print('Title:', title)
            print('Content:', content)
            print('Upvotes:', upvotes)
            print('Author:', author)
            print('Time:', post_timestamp)

        session.commit()
        session.close()


