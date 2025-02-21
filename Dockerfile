FROM python:3.9-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY . /app/
COPY .env ./

RUN poetry install --no-root

RUN poetry run python manage.py migrate && \
    poetry run python manage.py collectstatic --noinput

RUN poetry add gunicorn

EXPOSE 8000

CMD poetry run python -m smtpd -n -c DebuggingServer localhost:1025 & \
    poetry run python manage.py process_tasks & \
    poetry run gunicorn testapi.wsgi:application --bind 0.0.0.0:8000