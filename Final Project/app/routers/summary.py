from fastapi import APIRouter, HTTPException
from .. import database, crud, schemas, utility


router = APIRouter(
    prefix="/summaries",
    tags=["summaries"],
)

db = database.create_db_connection()
@router.post("/", response_model=schemas.Summary)
def create_summary(summary: schemas.SummaryFast):
    news_id = summary.news_id
    news_body = crud.get_news(db, news_id=news_id)["body"]

    summary_text = utility.generate_summary(news_body)
    return crud.insert_summary(db=db, news_id=news_id, summary_text=summary_text)


@router.get("/{summary_id}", response_model=schemas.Summary)
def read_summary(summary_id: int):
    print(summary_id)
    db_summary = crud.get_summary(db, summary_id=summary_id)
    if db_summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")
    return db_summary



