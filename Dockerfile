FROM python:3.12-slim-bookworm
LABEL creator="Roman Ivanov"
LABEL email="sitdoff@gmail.com"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.6.1
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"
WORKDIR /code
COPY poetry.lock pyproject.toml wait-for-it.sh entrypoint.sh .env /code/
RUN poetry config virtualenvs.create false && poetry install --only main&& chmod +x /code/entrypoint.sh
COPY ./us /code/
ENTRYPOINT [ "./entrypoint.sh", "python3", "manage.py", "runserver", "0.0.0.0:8000"]
