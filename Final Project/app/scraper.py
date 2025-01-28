import datetime
from requests_html import HTMLSession
from .crud import create_news
from .schemas import NewsCreate

def single_news_scraper(url: str):
    session = HTMLSession()
    try:
        response = session.get(url)
        # response.html.render()  # This will download Chromium if not found

        publisher_website = url.split('/')[2]
        publisher = publisher_website.split('.')[-2]
        title = response.html.find('h1.headline', first=True).text
        li_elements = response.html.find('section.article-info > div > div > ul.list-inline > li')
        reporter = li_elements[0].text 
        news_datetime = datetime.datetime.now()
        breadcrumb_items = response.html.find('ol.breadcrumb > li')
        category = breadcrumb_items[2].text 
        content = '\n'.join([p.text for p in response.html.find('p')])
        img_tags = response.html.find('figure.figure > img.img-responsive')
        images = [img.attrs['src'] for img in img_tags if 'src' in img.attrs]

        # print(f"Scraped news from {url}")
        # print(f"Title: {title}")
        # print(f"Reporter: {reporter}")
        # print(f"Date: {news_datetime}")
        # print(f"Category: {category}")
        # print(f"Images: {images}")


        return NewsCreate(
            publisher_website=publisher_website,
            news_publisher=publisher,
            title=title,
            news_reporter=reporter,
            datetime=news_datetime,
            link=url,
            news_category=category,
            body=content,
            images=images,
        )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def scrape_and_store_news(url: str, db):
    # db = SessionLocal()
    news_data = single_news_scraper(url)
    print(news_data)
    inserted_news = ""
    if news_data:
        inserted_news = create_news(db=db, news=news_data)
    # db.close()

    return inserted_news
