# Use official Python image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Ensure database persistence
VOLUME [ "/app/db" ]

# Expose port 8000
EXPOSE 8000

# Start Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project.wsgi:application"]
