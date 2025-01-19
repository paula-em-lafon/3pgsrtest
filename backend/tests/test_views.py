import os
import json
from fastapi import status
from fastapi.testclient import TestClient
from datetime import datetime as dt
import pytest
#  internals
from app.main import app
from app.database import create_tables,drop_tables, add_author, add_book
from app import models
from app.models import AuthorDB, AuthorSchema, BookDB, BookSchema

client = TestClient(app)


#  use test database and create tables
os.environ["DB_NAME"] = "booksAndAuthorsTest"
drop_tables()
create_tables()

def test_get_books():
    drop_tables()
    create_tables()
    response = client.get("/api")
    assert response.status_code == status.HTTP_200_OK
    drop_tables()

def test_get_books_with_data():
    drop_tables()
    create_tables()
    author_obj1 = {"author": "John Doe"}
    author1 = AuthorSchema(**{"author": "John Doe"})
    author_obj2 = {"author": "Jane Doe"}
    author2 = AuthorSchema(**{"author": "Jane Doe"})
    add_author(author1)
    add_author(author2)
    book_obj1 = {"title": "some title", "year": 2023, "status":"PUBLISHED", "author":2}
    book1 = BookSchema(**{"title": "some title", "year": 2023, "status":"PUBLISHED", "author":2})
    book_obj2 = {"title": "some title 2", "year": 1996, "status":"DRAFT", "author":1}
    book2 = BookSchema(**{"title": "some title 2", "year": 1996, "status":"DRAFT", "author":1})
    add_book(book1)
    add_book(book2)
    response = client.get("/api")
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert res_json["authors"][0]["author"] == author_obj1["author"]
    assert res_json["books"][1]["author"] == book_obj2["author"]
    drop_tables()

def test_add_book_with_new_author():
    drop_tables()
    create_tables()
    payload = {
        "title": "some title", "year": 2023, "status":"PUBLISHED", "author_name":"john doe"
    }
    expected = {
        'id': 1,
        "title": "some title", "year": 2023, "status":"PUBLISHED", "author":1
    }

    response = client.post('/api/newbook', data=json.dumps(payload))
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert res_json["id"] == expected["id"]
    assert res_json["title"] == expected["title"]
    assert res_json["year"] == expected["year"]
    assert res_json["status"] == expected["status"]
    assert res_json["author"] == expected["author"]

    response = client.post('/api/newbook',
                           json={'created_by': 'cb', 'context': 'ct'})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    drop_tables()

def test_add_book_with_existing_author():
    drop_tables()
    create_tables()
    author_obj1 = {"author": "John Doe"}
    author1 = AuthorSchema(**{"author": "John Doe"})
    add_author(author1)
    payload = {
        "title": "some title", "year": 2023, "status":"PUBLISHED", "author_id":1
    }
    expected = {
        'id': 1,
        "title": "some title", "year": 2023, "status":"PUBLISHED", "author":1
    }

    response = client.post('/api/newbook', data=json.dumps(payload))
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert res_json["id"] == expected["id"]
    assert res_json["title"] == expected["title"]
    assert res_json["year"] == expected["year"]
    assert res_json["status"] == expected["status"]
    assert res_json["author"] == expected["author"]

    response = client.post('/api/newbook',
                           json={'created_by': 'cb', 'context': 'ct'})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    drop_tables()

def test_edit_book_with_new_author():
    drop_tables()
    create_tables()
    author_obj1 = {"author": "John Doe"}
    author1 = AuthorSchema(**{"author": "John Doe"})
    add_author(author1)
    book_obj1 = {"title": "some title", "year": 2023, "status":"PUBLISHED", "author":1}
    book1 = BookSchema(**{"title": "some title", "year": 2023, "status":"PUBLISHED", "author":1})
    add_book(book1)
    payload = {
        "title": "some title edited", "year": 2000, "status":"DRAFT", "author_name": "Jane Doe"
    }
    expected = {
        'id': 1,
        "title": "some title edited", "year": 2000, "status":"DRAFT", "author":2
    }

    response = client.post('/api/editbook/1', data=json.dumps(payload))
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert res_json["id"] == expected["id"]
    assert res_json["title"] == expected["title"]
    assert res_json["year"] == expected["year"]
    assert res_json["status"] == expected["status"]
    assert res_json["author"] == expected["author"]

    response = client.post('/api/editbook/1',
                           json={'created_by': 'cb', 'context': 'ct'})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    drop_tables()

def test_edit_book_with_existing_author():
    drop_tables()
    create_tables()
    author_obj1 = {"author": "John Doe"}
    author1 = AuthorSchema(**{"author": "John Doe"})
    author_obj2 = {"author": "Jane Doe"}
    author2 = AuthorSchema(**{"author": "Jane Doe"})
    add_author(author1)
    add_author(author2)
    book_obj1 = {"title": "some title", "year": 2023, "status":"PUBLISHED", "author":1}
    book1 = BookSchema(**{"title": "some title", "year": 2023, "status":"PUBLISHED", "author":1})
    add_book(book1)
    payload = {
        "title": "some title edited", "year": 2000, "status":"DRAFT", "author_id":2
    }
    expected = {
        'id': 1,
        "title": "some title edited", "year": 2000, "status":"DRAFT", "author":2
    }

    response = client.post('/api/editbook/1', data=json.dumps(payload))
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert res_json["id"] == expected["id"]
    assert res_json["title"] == expected["title"]
    assert res_json["year"] == expected["year"]
    assert res_json["status"] == expected["status"]
    assert res_json["author"] == expected["author"]

    response = client.post('/api/editbook/1',
                           json={'created_by': 'cb', 'context': 'ct'})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    drop_tables()