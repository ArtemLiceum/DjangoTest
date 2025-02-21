FROM python:3.9-slim

WORKDIR /app

RUN pip install poetry &&\
    export PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . /app/

RUN poetry run python manage.py migrate && \
    poetry run python manage.py collectstatic --noinput

RUN poetry add gunicorn

EXPOSE 8000

CMD poetry run python -m smtpd -n -c DebuggingServer localhost:1025 & \
    poetry run python manage.py process_tasks & \
    poetry run gunicorn testapi.wsgi:application --bind 0.0.0.0:8000