import psycopg2
from psycopg2 import sql

def create_databases():
    db_params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "password",
        "host": "db",  # Correct hostname
        "port": 5432
    }

    databases = ["booksAndAuthors", "booksAndAuthorsTest"]

    conn = None  # Initialize the connection to avoid UnboundLocalError

    try:
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cursor = conn.cursor()

        for db_name in databases:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            exists = cursor.fetchone()

            if exists:
                print(f"Database '{db_name}' already exists.")
            else:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                print(f"Database '{db_name}' created successfully.")

        cursor.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_databases()
