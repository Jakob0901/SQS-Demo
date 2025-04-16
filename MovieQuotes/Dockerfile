# Use the official Python image as the base image
FROM python:3.11-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir .

# Expose port 80
EXPOSE 80

# Set the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

# Run the Flask application
CMD ["flask", "run"]