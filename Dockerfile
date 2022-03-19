FROM python:3.10.2

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -u 1000 -d /app -M -s /bin/false app \
	&& pip install poetry gunicorn
ENV POETRY_VIRTUALENVS_CREATE=false

COPY . /app/
WORKDIR /app/

RUN poetry install --no-dev --no-interaction \
	&& python manage.py collectstatic --no-input

USER 1000
CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:8000", "-t", "300", "--threads", "16", "send.wsgi:application"]
