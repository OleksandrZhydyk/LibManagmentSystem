from dependencies.service import get_genre_service
from fastapi import APIRouter, Depends, HTTPException
from logger import get_logger
from schemas.exception import HTTPExceptionResponse
from schemas.genre import GenreCreateRequest, GenreCreateResponse
from services.genre import GenreService

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "",
    response_model=GenreCreateResponse,
    responses={409: {"model": HTTPExceptionResponse, "description": "Genre already exists."}},
)
async def create_genre(
    genre_create: GenreCreateRequest,
    service: GenreService = Depends(get_genre_service),
):
    try:
        genre = await service.create_genre(genre_create)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    return genre


@router.get("", response_model=list[GenreCreateResponse])
async def get_genres(service: GenreService = Depends(get_genre_service)):
    logger.info("get genres")
    return await service.get_all()
