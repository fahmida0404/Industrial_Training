import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
gro_api_key=os.getenv("GROQ_API_KEY")

def generate_summary(news_body):
    client = Groq()
    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are expert in news summarization in bengali languages. Please summarize the following news article in top  3-5 bullet points in the bengali language that you get."
            },
            {
                "role": "user",
                "content": news_body
            }
        ],
        temperature=0,
        max_tokens=32768,
        top_p=1,
        stream=False,
        stop=None,
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content
