from database.models import User
from dependencies.auth import get_current_active_user
from dependencies.service import get_borrow_service
from fastapi import APIRouter, Depends, HTTPException
from schemas.borrows import BookReturnRequest, BorrowCreateRequest, BorrowResponse
from schemas.exception import HTTPExceptionResponse
from services.borrows import BorrowService

router = APIRouter()


@router.post(
    "/borrow",
    response_model=BorrowResponse,
    responses={404: {"model": HTTPExceptionResponse, "description": "Book is not free or not exists."}},
)
async def borrow_book(
    borrow_create: BorrowCreateRequest,
    user: User = Depends(get_current_active_user),
    service: BorrowService = Depends(get_borrow_service),
):
    try:
        borrow = await service.borrow(borrow_create, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return borrow


@router.post(
    "/return",
    response_model=BorrowResponse,
    responses={
        404: {
            "model": HTTPExceptionResponse,
            "description": "User didn't get a book, borrow history data was not found.",
        }
    },
)
async def return_book(
    book_return: BookReturnRequest,
    user: User = Depends(get_current_active_user),
    service: BorrowService = Depends(get_borrow_service),
):
    try:
        borrow = await service.book_return(book_return, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return borrow
