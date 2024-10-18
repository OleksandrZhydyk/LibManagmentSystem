from database.models import Book
from fastapi_filter.contrib.sqlalchemy import Filter


class BookFilter(Filter):
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = Book
        ordering_field_name = "order_by"
