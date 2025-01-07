from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

my_app = FastAPI(
    title = "AI News API",
    description = "This is an API consisting of news related to Artificial Intelligence and its branches.", 
    contact ={
        "name": "Fahmida Akter",
        "email": "fahmida0404@gmail.com",
    }
)

news = {
    1:
    {
        "id": 1,
        "title":  "Difference between AI, ML, LLM, and Generative AI",
        "content": "Artificial Intelligence (AI), Machine Learning (ML), Large Language Models (LLMs), and Generative AI are all related concepts in the field of computer science.",
        "author": "Toloka Team"
    },

    2:
    {
        "id": 2,
        "title":  "Understanding Artificial Intelligence Hierarchy",
        "content": "The connections between key AI concepts like Machine Learning (ML), Generative AI(GEN AI), and Large Language Models(LLM).",
        "author": "Ansam Yousry"
    },

        3:
    {
        "id": 3,
        "title":  "What is an LLM? A Guide on Large Language Models and How They Work",
        "content": "What LLMs are, how they work, the different types of LLMs with examples, as well as their advantages and limitations.",
        "author": "Javier Canales Luna"
    },

        4:
    {
        "id": 4,
        "title":  "What is machine learning? Guide, definition and examples",
        "content": "Machine learning is a branch of AI focused on building computer systems that learn from data.",
        "author": "Lev Craig"
    },

        5:
    {
        "id": 5,  
        "title":  "Generative AI: Navigating the Course to the Artificial General Intelligence Future",
        "content": "Generative AI creates new content, like text or images, based on patterns in data.",
        "author": "Martin Musiol"
    }
}

class News(BaseModel):
    title: str
    content: str | None = None
    author: str

@my_app.get("/news")
def my_news():
    return news

# @my_app.get("/news{author}")
# def news_by_author(author: str):
#     news_of_author = [news for news in news.values() if news["author"].lower() == author.lower()]
#     if not news_of_author:
#         return{"data": f"No news by the author {author}"}
    # return news_of_author

# @my_app.get("/news{id}")
# def news_by_id(id: int):
#     if id not in news:
#         return{"data": f"No news of id {id}"}
#     return news[id]

@my_app.get("/news{author}")
def news_by_author_title(author: str, title: str = None):
    selected_news = [news for news in news.values() if news["author"].lower() == author.lower()]
    if not selected_news:
        return{"data": f"No news by the author {author}"}
    if title:
        selected_news = [news for news in news.values() if news["title"].lower() == title.lower()]
    return selected_news

@my_app.post("/add_news")
def add_news(new_news: News):
    print(new_news)

    id = max(news.keys()) + 1
    news[id] = {
        "id": id,  
        "title":  new_news.title,
        "content": new_news.content,
        "author": new_news.author
    }

    return news[id]


@my_app.get("/")
def root():
    return {"message": "Welcome to News API"}

if __name__ == "__main__":
    uvicorn.run("my_app:my_app", host = "localhost", port = 8000, reload = True )
    