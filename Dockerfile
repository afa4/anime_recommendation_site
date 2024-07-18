# Use the official Python base image
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./anime_recommendation_site .
COPY ./malprofile .
COPY manage.py .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
