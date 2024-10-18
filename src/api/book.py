from dependencies.service import get_book_service
from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from fastapi_pagination import LimitOffsetPage
from filters import BookFilter
from schemas.book import BookCreateRequest, BookResponse
from schemas.borrows import BorrowResponse
from schemas.exception import HTTPExceptionResponse
from services.book import BookService

router = APIRouter()


@router.post(
    "",
    response_model=BookResponse,
    responses={409: {"model": HTTPExceptionResponse, "description": "Book already exists."}},
)
async def create_book(
    book_create: BookCreateRequest,
    service: BookService = Depends(get_book_service),
):
    try:
        book = await service.create_book(book_create)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    return book


@router.get("", response_model=LimitOffsetPage[BookResponse])
async def get_books(
    service: BookService = Depends(get_book_service), user_ordering: BookFilter = FilterDepends(BookFilter)
) -> LimitOffsetPage[BookResponse]:
    return await service.get_all(user_ordering)


@router.get("/{pk}/history", response_model=list[BorrowResponse])
async def get_book_history(pk: int, service: BookService = Depends(get_book_service)):
    return await service.get_book_history(pk)
