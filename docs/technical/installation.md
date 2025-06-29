# Installation Guide

## Docker Compose

This project can be run using Docker Compose, which simplifies the setup and management of the application and its dependencies.

### Prerequisites
- Docker and Docker Compose installed on your machine.

### Start Docker Compose

```bash
cd docker-compose
./start-compose.sh
```
This command starts the Docker Compose setup, which includes the application and its dependencies.
It also generates the necessary environment variables for the application to run.

## Docker Container

This project can be run using Docker Compose, which simplifies the setup and management of the application and its dependencies.
Alternatively, you can run the application in a Docker container directly.

### Prerequisites
- Docker installed on your machine.
- PostgreSQL database (preferred version 15 or higher).

### Github Container Registry

```bash
docker pull ghcr.io/jakob0901/sqs-demo:latest
docker run -d -p 80:80 ghcr.io/jakob0901/sqs-demo:latest
```

This command pulls the latest image from the GitHub Container Registry and runs it, exposing port 80.
Further configuration can be done via environment variables.

### Local Image Build

```bash
cd QuoteService
docker build -t sqs-demo:latest .
docker run -d -p 80:80 sqs-demo:latest
```

This command builds the Docker image from the local `Dockerfile` and runs it, exposing port 80.
Further configuration can be done via environment variables.

## Local/Native Execution

This project can be executed outside the Docker environment. 
The following steps outline how to set up and run the application locally.

### Prerequisites
- Python 3.10 or higher
- PostgreSQL database (preferred version 15 or higher)
- Virtual environment (optional but recommended)
- Required environment variables: (adjust as needed)
  - `PYTHONUNBUFFERED=1`
  - `API_KEY=secure`
  - `DB_USERNAME=user`
  - `DB_PASSWORD=kernschmelze`
  - `DATABASE_URL=localhost:5432/app_db`
  
### Install Dependencies

```bash
cd QuoteService
pip install -r .
```

This command installs the dependencies listed in the `setup.py` file.

### start the application

```bash
cd QuoteService
python3 app.py
```

This starts the Flask application on `http://localhost:80`.
