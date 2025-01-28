from fastapi import APIRouter, HTTPException
from typing import List
from .. import  database, crud, schemas, scraper
router = APIRouter(
    prefix="/news",
    tags=["news"],
)

db = database.create_db_connection()

@router.get("/", response_model=List[schemas.News])
def read_news_list(skip: int = 0, limit: int = 3):
    """
    Return all news from the database.
    """
    news_list = crud.get_news_list(db=db, skip=skip, limit=limit)
    if not news_list:
        raise HTTPException(status_code=404, detail="News not found")
    return news_list


@router.get("/{news_id}", response_model=schemas.News)
def read_news(news_id: int):
    news = crud.get_news(db, news_id=news_id)

    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return news




@router.post("/scrape/", response_model=List[schemas.News])
def scrape_news(urls: List[str]):
    all_inserted_news = []
    for url in urls:
        inserted_news = scraper.scrape_and_store_news(url, db)
        all_inserted_news.append(inserted_news)
    return all_inserted_news



