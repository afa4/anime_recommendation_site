# Use the official Python base image
FROM python:3.9-slim

# Set environment variables for production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY ./anime_recommendation_site anime_recommendation_site
COPY ./malprofile ./malprofile
COPY manage.py .

# Expose the port
EXPOSE 8000

# Start Nginx and Gunicorn
CMD gunicorn anime_recommendation_site.wsgi:application --bind 0.0.0.0:8000 --timeout 120
