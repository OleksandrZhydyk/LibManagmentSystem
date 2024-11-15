FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /server
ENV ENV_FILE_PATH="../.env"

RUN apt-get update && apt-get install gettext -y
RUN python -m pip install --upgrade pip && pip install poetry

COPY ./pyproject.toml .

RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install --no-root --only main

COPY ./src ./src
COPY ./migrations ./migrations
COPY ./alembic.ini ./alembic.ini
COPY ./script ./script

RUN chmod a+x ./script/run_server.sh

EXPOSE 8000

CMD ["bash"]
