#Mysql CRUD operations to insert data into database or fetch data from databse

def get_news_list(db, skip: int = 0, limit: int = 3):
    query = """
        SELECT *
        FROM news
        ORDER BY datetime DESC
        LIMIT %s OFFSET %s;
    """
    with db.cursor() as cursor:
        cursor.execute(query, (limit, skip))
        result = cursor.fetchall()
    
    # Map the raw database result (tuples) to a list of dictionaries
    news_list = [
        {
            "id": row[0],
            "datetime": row[1],
            "title": row[2],
            "body": row[3],
            "link": row[4],
            "category_id": row[5],
            "reporter_id": row[6],
            "publisher_id": row[7],
        }
        for row in result
    ]
    
    return news_list


def get_news(db, news_id: int):
    # print(db, news_id)
    query = """
        SELECT *
        FROM News
        WHERE id = %s
        LIMIT 1;
    """
    with db.cursor() as cursor:
        cursor.execute(query, (news_id,))
        result = cursor.fetchone()
                
    if result is None:
        return None 
    
    news = {
            "id": result[0],
            "datetime": result[1],
            "title": result[2],
            "body": result[3],
            "link": result[4],
            "category_id": result[5],
            "reporter_id": result[6],
            "publisher_id": result[7],
        }
    return news


def get_or_create_category(db, name: str, description: str):
    query = """
        SELECT * FROM categories WHERE name = %s
    """
    with db.cursor() as cursor:
        cursor.execute(query, (name,))
        category = cursor.fetchone()

        if category is None:
            insert_query = """
                INSERT INTO categories (name, description) VALUES (%s, %s)
            """
            cursor.execute(insert_query, (name, description))
            db.commit()
            cursor.execute(query, (name,))  # Fetch the inserted category
            category = cursor.fetchone()

    return category

def get_or_create_reporter(db, name: str, email: str):
    query = """
        SELECT * FROM reporters WHERE name = %s
    """
    with db.cursor() as cursor:
        cursor.execute(query, (name,))
        reporter = cursor.fetchone()

        if reporter is None:
            insert_query = """
                INSERT INTO reporters (name, email) VALUES (%s, %s)
            """
            cursor.execute(insert_query, (name, email))
            db.commit()
            cursor.execute(query, (name,))  # Fetch the inserted reporter
            reporter = cursor.fetchone()

    return reporter

def get_or_create_publisher(db, name: str, website: str):
    query = """
        SELECT * FROM publishers WHERE name = %s
    """
    with db.cursor() as cursor:
        cursor.execute(query, (name,))
        publisher = cursor.fetchone()

        if publisher is None:
            insert_query = """
                INSERT INTO publishers (name, website) VALUES (%s, %s)
            """
            cursor.execute(insert_query, (name, website))
            db.commit()
            cursor.execute(query, (name,))  # Fetch the inserted publisher
            publisher = cursor.fetchone()

    return publisher

def get_news_existance(db, news_title: str):
    query = """
        SELECT * FROM news WHERE title = %s
    """
    with db.cursor() as cursor:
        cursor.execute(query, (news_title,))
        return cursor.fetchone()

def create_image(db, news_id: int, url: str):
    query = """
        INSERT INTO images (news_id, url) VALUES (%s, %s)
    """
    with db.cursor() as cursor:
        cursor.execute(query, (news_id, url))
        db.commit()

def create_news(db, news):
    # print(f"Inserting news:")
    
    # Retrieve or create related entities
    category = get_or_create_category(db, news.news_category, f"{news.news_category} description")
    reporter = get_or_create_reporter(db, news.news_reporter, f"{news.news_reporter}@example.com")
    publisher = get_or_create_publisher(db, news.news_publisher, f"https://{news.publisher_website}")
    
    # Check if the news already exists
    news_exist = get_news_existance(db, news_title=news.title)
    if news_exist:
        print("News already exists:", news_exist)
        return news_exist

    print(category[1], reporter[1], publisher[1])  # Assuming the second column is the name
    
    # Insert new news into the database
    insert_query = """
        INSERT INTO news (title, datetime, body, link, category_id, reporter_id, publisher_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    with db.cursor() as cursor:
        cursor.execute(insert_query, (
            news.title,
            news.datetime,
            news.body,
            news.link,
            category[0],  # Assuming the first column is the ID
            reporter[0],
            publisher[0]
        ))
        db.commit()
        news_id = cursor.lastrowid

    # Add images associated with the news id
    for image_url in news.images:
        create_image(db, news_id=news_id, url=image_url)

    return {
        "id": news_id,
        "title": news.title,
        "datetime": news.datetime,
        "body": news.body,
        "link": news.link,
        "category_id": category[0],
        "reporter_id": reporter[0],
        "publisher_id": publisher[0],
    }


def insert_summary(db, news_id: int, summary_text: str):

    insert_query = "INSERT INTO summaries (news_id, summary_text) VALUES (%s, %s);"
    
    with db.cursor() as cursor:
        cursor.execute(insert_query, (news_id, summary_text))
        db.commit()
        summary_id = cursor.lastrowid

    summary_dict = {
        "id": summary_id,
        "news_id": news_id,
        "summary_text": summary_text

    }
    return summary_dict 




def get_summary(db, summary_id: int):
    query = "SELECT * FROM summaries WHERE id = %s;"
    
    with db.cursor() as cursor:
        cursor.execute(query, (summary_id,))
        summary = cursor.fetchone()  # Fetches the first matching row
    
    if summary is None:
        return None
    
    summary_dict = {
        "id": summary[0],
        "news_id": summary[1],
        "summary_text": summary[2]

    }
    return summary_dict 

