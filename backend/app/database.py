import os
from pathlib import Path
import dotenv
from abc import ABC, abstractmethod
from app.models import AuthorDB, AuthorSchema, BookDB, BookSchema
import psycopg2

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(BASE_DIR / ".env")

class Database(ABC):
    """
    Database context manager
    """

    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()

    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()

class PgDatabase(Database):
    """PostgreSQL Database context manager"""

    def __init__(self) -> None:
        self.driver = psycopg2
        super().__init__(self.driver)

    def connect_to_database(self):
        return self.driver.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
    
t_authors = "t_authors"
t_books = "t_books"

def create_tables():
    with PgDatabase() as db:
        db.cursor.execute(f"""CREATE TABLE {t_authors} (
            id SERIAL PRIMARY KEY,
            author VARCHAR(140)
            );
        """)
        db.connection.commit()
        db.cursor.execute(f"""
            CREATE TYPE status_enum AS ENUM ('PUBLISHED', 'DRAFT');
        """)
        db.connection.commit()
        db.cursor.execute(f"""CREATE TABLE {t_books} (
            id SERIAL PRIMARY KEY,
            title VARCHAR(140),
            year INT,
            status status_enum NOT NULL DEFAULT 'DRAFT',
            author INT NOT NULL,
            CONSTRAINT fk_author FOREIGN KEY (author) REFERENCES {t_authors} (id) ON DELETE CASCADE
            );
        """)
        db.connection.commit()
        print("Tables are created successfully...")

def drop_tables():
    with PgDatabase() as db:
        db.cursor.execute(f"DROP TABLE IF EXISTS {t_books} CASCADE;")
        db.connection.commit()
        db.cursor.execute(f"DROP TYPE IF EXISTS status_enum;")
        db.connection.commit()
        db.cursor.execute(f"DROP TABLE IF EXISTS {t_authors} CASCADE;")
        db.connection.commit()
        print("Tables are dropped...")

def fetch_all_authors() -> list:
    with PgDatabase() as db:
        db.cursor.execute("""
        SELECT id, author FROM t_authors;
        """)
        data = db.cursor.fetchall()

    if not data:
        return []

    return [{"id": row[0], "author": row[1]} for row in data]

def fetch_all_books() -> list:
    with PgDatabase() as db:
        db.cursor.execute("""
        SELECT 
            b.id, 
            b.title, 
            b.year, 
            b.status, 
            b.author
        FROM t_books b
        """)
        data = db.cursor.fetchall()

    if not data:
        return []

    return [
        {
            "id": row[0],
            "title": row[1],
            "year": row[2],
            "status": row[3],
            "author": row[4]
        }
        for row in data
    ]

def select_t_book_by_id(id: int) -> dict:
    with PgDatabase() as db:
        db.cursor.execute(f"""
        SELECT id, title, year, status, author FROM t_books
        WHERE id={id};
                        """)
        data = db.cursor.fetchone()
        if data is None:
            return {"error": "Book not found"}

    return {
        "id": data[0],
        "title": data[1],
        "year": data[2],
        "status": data[3],
        "author": data[4]
    }

def add_author(payload: AuthorSchema, *args, **kwargs) -> dict:
    try:
        with PgDatabase() as db:
            # Insert the author into the {t_authors} table

            db.cursor.execute("""
            INSERT INTO t_authors (author) VALUES (%s) RETURNING id, author;
            """, (payload.author,))
            db.connection.commit()
            new_author = db.cursor.fetchone()

        # Return the newly added author's details
        return {
            "id": new_author[0],
            "author": new_author[1]
        }

    except Exception as e:
        print(f"Error adding author: {e}")
        return {"error": str(e)}
    
def add_book(payload: BookSchema, *args, **kwargs) -> dict:
    try:
        with PgDatabase() as db:
            # Insert the book into the books table
            db.cursor.execute("""
            INSERT INTO t_books (title, year, status, author)
            VALUES (%s, %s, %s, %s)
            RETURNING id, title, year, status, author;
            """, (payload.title, payload.year,
                   payload.status, payload.author))
            db.connection.commit()
            new_book = db.cursor.fetchone()

        # Return the newly added book's details
        return {
            "id": new_book[0],
            "title": new_book[1],
            "year": new_book[2],
            "status": new_book[3],
            "author": new_book[4]
        }

    except Exception as e:
        print(f"Error adding book: {e}")
        return {"error": str(e)}
    
def edit_book(id: int, payload: BookSchema) -> dict:
    try:
        # Use parameterized queries to avoid SQL injection
        query = f"""
            UPDATE {t_books}
            SET 
                title = %s, 
                year = %s, 
                status = %s,
                author= %s
            WHERE id = %s
            RETURNING id, title, year, status, author;
        """

        # Extract the Enum value for the `status` field
        values = (payload.title, payload.year, payload.status.value, payload.author, id)

        # Execute the query
        with PgDatabase() as db:
            db.cursor.execute(query, values)
            result = db.cursor.fetchone()
            db.connection.commit()

        if not result:
            return {"error": "Book not found"}

        # Return the updated book details
        return {
            "id": result[0],
            "title": result[1],
            "year": result[2],
            "status": result[3],
            "author": result[4],
        }

    except Exception as e:
        print(f"Error editing book: {e}")
        return {"error": str(e)}
    
 
 # Test create book

# if __name__ == "__main__":
#     # Example usage of the add_book function
#     test_book = {"title": "some title", "year": 2023, "status":"PUBLISHED", "author":3}

#     # Validate the data using the schema
#     test_book = BookSchema(**test_book)
#     new_book = add_book(test_book)
#     if "error" in new_book:
#         print(f"Failed to add book: {new_book['error']}")
#     else:
#         print(f"Book added successfully: {new_book}")


# Test fetch all authors

# if __name__ == "__main__":
#     authors = fetch_all_authors()
#     for author in authors:
#         print(author)

# Test create Author

# if __name__ == "__main__":
#     # Example usage of the add_author function
#     # Example data for testing
#     test_author = {"author": "John Doe"}

#     # Validate the data using the schema
#     author = AuthorSchema(**test_author)

#     new_author = add_author(author)
#     if "error" in new_author:
#         print(f"Failed to add author: {new_author['error']}")
#     else:
#         print(f"Author added successfully: ID={new_author['id']}, Name={new_author['author']}")

# Test fetch all books

# if __name__ == "__main__":
#     books = fetch_all_books()
#     for book in books:
#         print(book)

# Test Edit book

# if __name__ == "__main__":
#     test_book = {"title": "an edited title", "year": 2001, "status":"DRAFT", "author":4}

#     # Validate the data using the schema
#     test_book = BookSchema(**test_book)
#     updated_book = edit_book(3, test_book)
#     if "error" in updated_book:
#         print(f"Failed to edit book: {updated_book['error']}")
#     else:
#         print(f"Book updated successfully: {updated_book}")

# Test Get Book

# if __name__ == "__main__":
    
#     retrieved_book = select_t_book_by_id(3)
#     if "error" in retrieved_book:
#         print(f"Failed to edit book: {retrieved_book['error']}")
#     else:
#         print(f"Book fetched successfully: {retrieved_book}")