from fastapi import APIRouter

from .auth import router as auth_router
from .author import router as author_router
from .book import router as book_router
from .borrows import router as borrows_router
from .genre import router as genre_router
from .publisher import router as publisher_router

api_router = APIRouter()

api_router.include_router(genre_router, prefix="/genres", tags=["Genres"])
api_router.include_router(publisher_router, prefix="/publishers", tags=["Publishers"])
api_router.include_router(author_router, prefix="/authors", tags=["Authors"])
api_router.include_router(book_router, prefix="/books", tags=["Books"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(borrows_router, prefix="", tags=["Borrows"])
