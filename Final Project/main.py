from fastapi import FastAPI
import uvicorn

from app.routers import news, summary


app = FastAPI(

    title="News Summarizing API",
    description="This is the API documentation for news scraping and summarizing using AI (Llama).",
    contact={
        "name": "Fahmida Akter",
        "email": "fahmidaakter0404@gmail.com",
    },
    redoc_url="/details",
    docs_url="/execute",
)

app.include_router(news.router)
app.include_router(summary.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the News Summarizing API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
    # uvicorn.run("main:app", host="localhost", port=8011, reload=True)