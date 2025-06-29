# Project Overview

## Directory Structure

### .github

Contains GitHub Actions workflows for CI/CD. Refer to [testing.md](testing.md) for details on the workflows.

### docs
Contains documentation files, including arc42, adrs, installation guides, testing instructions, and project structure details.
It also contains the source files for the plantuml files used to generate the images used in the documentation.
The contents are rendered on [Read the Docs](https://sqs-demo.readthedocs.io/).

### docker-compose

Contains the `docker-compose.yml` file for running the application and its dependencies in a Docker environment. 
This setup simplifies the management of the application and its services.
It also contains the Dockerfile for building the application image inside the pipeline and compose.
The `start-compose.sh` or `start-compose.bat` script is used to start the Docker Compose setup.

### QuoteService

Contains the main application code, including the Flask app, routes, and business logic.

- database: Contains the database abstraction.
- models: Contains the data models used in the application.
- static: Contains static files served by the Flask application(frontend).
- tests: Contains unit, integration, and end-to-end tests for the application.
- wrapper: Contains the application wrapper for external apis.
- app.py: The main entry point for the Flask application.
- setup.py: The setup script for installing the application and its dependencies.
- Dockerfile: The Dockerfile for building the application image outside the pipeline.
- .dockerignore: Specifies files and directories to ignore when building the Docker image.
- .coveragerc: Configuration file for coverage.py, specifying which files to include or exclude from coverage reports.
- __init__.py: Marks the directory as a Python package.

### additional_files

Contains additional files used for readTheDocs, Readme, License and git configuration.