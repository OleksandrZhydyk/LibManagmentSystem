from dependencies.service import get_author_service
from fastapi import APIRouter, Depends, HTTPException
from schemas.author import AuthorCreateRequest, AuthorResponse
from schemas.book import BookResponse
from schemas.exception import HTTPExceptionResponse
from services.author import AuthorService

router = APIRouter()


@router.post(
    "",
    response_model=AuthorResponse,
    responses={409: {"model": HTTPExceptionResponse, "description": "Author already exists."}},
)
async def create_author(
    author_create: AuthorCreateRequest,
    service: AuthorService = Depends(get_author_service),
):
    try:
        author = await service.create_author(author_create)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    return author


@router.get("", response_model=list[AuthorResponse])
async def get_authors(service: AuthorService = Depends(get_author_service)):
    return await service.get_all()


@router.get(
    "/{pk}/books",
    response_model=list[BookResponse],
    responses={404: {"model": HTTPExceptionResponse, "description": "Author doesn't exist."}},
)
async def get_author_books(pk: int, service: AuthorService = Depends(get_author_service)):
    try:
        books = await service.get_author_books(pk)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return books
