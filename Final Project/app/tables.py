from database import create_db_connection

def execute_query(connection, query,name):
    """
    Execute SQL query to on the database connection.

    Returns
    -------
    None
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print(f"{name} table created successful")
    except Exception as e:
        print(f"The error '{e}' occurred")

def create_tables():
    """
    Create tables in the database based on the predefined schema.


    Returns
    -------
    None
    """

    connection = create_db_connection()

    create_categories_table = """
    CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        description VARCHAR(255)
    );
    """

    create_reporters_table = """
    CREATE TABLE IF NOT EXISTS reporters (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL
    );
    """

    create_publishers_table = """
    CREATE TABLE IF NOT EXISTS publishers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        website VARCHAR(255) UNIQUE
    );
    """

    create_news_table = """
    CREATE TABLE IF NOT EXISTS news (
        id INT AUTO_INCREMENT PRIMARY KEY,
        datetime DATETIME NOT NULL,
        title VARCHAR(255),
        body TEXT,
        link VARCHAR(255),
        category_id INT,
        reporter_id INT,
        publisher_id INT,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
        FOREIGN KEY (reporter_id) REFERENCES reporters(id) ON DELETE SET NULL,
        FOREIGN KEY (publisher_id) REFERENCES publishers(id) ON DELETE SET NULL
    );
    """

    create_images_table = """
    CREATE TABLE IF NOT EXISTS images (
        id INT AUTO_INCREMENT PRIMARY KEY,
        news_id INT,
        url VARCHAR(255),
        FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE
    );
    """

    create_summaries_table = """
    CREATE TABLE IF NOT EXISTS summaries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        news_id INT,
        summary_text TEXT,
        FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE
    );
    """
    execute_query(connection, create_categories_table,"Category")
    execute_query(connection, create_reporters_table,"Reporter")
    execute_query(connection, create_publishers_table,"Publisher")
    execute_query(connection, create_news_table,"News")
    execute_query(connection, create_images_table,"Image")
    execute_query(connection, create_summaries_table,"Summary")


#Create tables if not exists through this code
if __name__ == '__main__':
    create_tables()