from dependencies.service import get_publisher_service
from fastapi import APIRouter, Depends, HTTPException
from schemas.exception import HTTPExceptionResponse
from schemas.publisher import PublisherCreateRequest, PublisherResponse
from services.publisher import PublisherService

router = APIRouter()


@router.post(
    "",
    response_model=PublisherResponse,
    responses={409: {"model": HTTPExceptionResponse, "description": "Publisher already exists."}},
)
async def create_publisher(
    publisher_create: PublisherCreateRequest,
    service: PublisherService = Depends(get_publisher_service),
):
    try:
        publisher = await service.create_publisher(publisher_create)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    return publisher


@router.get("", response_model=list[PublisherResponse])
async def get_publishers(
    service: PublisherService = Depends(get_publisher_service),
):
    return await service.get_all()
