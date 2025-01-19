from typing import List # new
from fastapi import APIRouter, HTTPException, status, Path
from psycopg2.errors import DatetimeFieldOverflow, OperationalError # new
#  internals
from app.database import (fetch_all_authors, fetch_all_books, add_author,add_book, edit_book) # new
from app.models import GetAllSchema, BookDB, BookSchema, AuthorDB, AuthorSchema, NewBookSchema

router = APIRouter()

# previous codes...

@router.get('/', response_model=GetAllSchema, status_code=status.HTTP_200_OK)
async def get_books_and_authors():
    try:
        allAuthors = fetch_all_authors();
        allBooks = fetch_all_books();
        return {"authors": allAuthors, "books": allBooks}
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="""Check if the database exists, connection is successful or tables exist. To create tables use '/initdb' endpoint"""
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"""Error {e}"""
        )
    
@router.post('/newbook', response_model=BookDB, status_code=status.HTTP_200_OK)
async def new_book(payload: NewBookSchema):
    try:
        newPayload = None;
        if payload.author_name and not payload.author_id:
            newAuthor = {"author": payload.author_name}
            checkedNewAuthor = AuthorSchema(**newAuthor)
            
            newAuthor = add_author(checkedNewAuthor)
            newAuthor = newAuthor["id"]
            newPayload = {"title": payload.title, "year": payload.year, "status":payload.status, "author":newAuthor}
        else:
            newPayload ={"title": payload.title, "year": payload.year, "status":payload.status, "author":payload.author_id}
        newPayload = BookSchema(**newPayload)
        return add_book(newPayload)
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="""Check if the database exists, connection is successful or tables exist. To create tables use '/initdb' endpoint"""
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"""Error {e}"""
        )
    
@router.post('/editbook/{id}/', response_model=BookDB, status_code=status.HTTP_200_OK)
async def change_book(payload: NewBookSchema, id: int = Path(..., gt=0)):
    try:
        newPayload = None;
        print("----------------PAYLOAD--------------")
        print(payload)
        if payload.author_name and not payload.author_id:
            newAuthor = {"author": payload.author_name}
            checkedNewAuthor = AuthorSchema(**newAuthor)
            
            newAuthor = add_author(checkedNewAuthor)
            newAuthor = newAuthor["id"]
            newPayload = {"title": payload.title, "year": payload.year, "status":payload.status, "author":newAuthor}
        else:
            newPayload ={"title": payload.title, "year": payload.year, "status":payload.status, "author":payload.author_id}
        newPayload = BookSchema(**newPayload)
        return edit_book(id, newPayload)
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="""Check if the database exists, connection is successful or tables exist. To create tables use '/initdb' endpoint"""
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"""Error {e}"""
        )