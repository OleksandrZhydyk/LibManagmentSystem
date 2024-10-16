# Use an official Python image as the base image
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /server

RUN apt-get update && apt-get install gettext -y
RUN python -m pip install --upgrade pip && pip install poetry

COPY ./pyproject.toml .

RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install --no-root --only main

COPY ./src ./src
COPY ./migrations ./migrations
COPY ./alembic.ini ./alembic.ini

EXPOSE 8000

# Command to run FastAPI with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
