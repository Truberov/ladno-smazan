FROM python:3.10-buster

WORKDIR /code

RUN pip install poetry pysqlite3-binary

RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --no-root --no-directory

COPY ./app ./app

CMD python3 -m app