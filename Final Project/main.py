from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from app.routers import news, summary
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="News Summarizing API",
    version="0.2",
    description="This is the API created for News Scraping and Summarizing through Llama.",
    contact={
        "name": "Fahmida Akter",
        "email": "fahmidaakter0404@gmail.com",
    },
    redoc_url="/documentation",
    docs_url="/execute",
)

# Define CORS settings
origins = ["*"]  # Allow requests from any origin

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(news.router)
app.include_router(summary.router)

@app.get("/")
def read_root():
    return {"message": "Welcome!"}


@app.get("/html", response_class=HTMLResponse)
def html_message():
    message = '''
    <div style=" text-align: center; padding: 100px;  color: teal; font-size: 36px;">
        Welcome to the News Summarizing API!<br>
        Created by: Fahmida Akter (C201221).
    </div>
    '''
    return message

if __name__ == "__main__":

    uvicorn.run("main:app", host="localhost", port=3000, reload=True)
