# Testing

## Prerequisites

See the [Installation Guide](installation.md) for prerequisites and setup instructions.
Refer to the Section about local/native execution for details on how to run the application outside of Docker.

A Database is required for integration and end-to-end tests.
You can use the provided Docker Compose setup to start a test database.
The docker-compose.yml file is located in the `tests` directory.
The PostgreSQL database should be running on `localhost:5432` with the name `app_db`.

## Unit Tests

Unit tests are designed to test individual components of the application in isolation.
Run the following command to execute the unit tests:

```bash
cd QuoteService/tests/unit
python3 -m unittest discover -s . -p "*.py"
```

## Integration Tests

Integration tests check the interaction between different components of the application.
Run the following command to execute the integration tests:

```bash
cd QuoteService/tests/integration
python3 -m unittest discover -s . -p "*.py"
```

## End-to-End Tests

End-to-end tests simulate real user scenarios to ensure the application works as expected.
Run the following command to execute the end-to-end tests:

```bash
cd QuoteService/
pip install pytest-playwright requests
playwright install --with-deps
python app.py &
# wait for the app to start
pytest tests/e2e -v
```

## Static Analysis

Static analysis tools help identify potential issues in the codebase without executing it.
The project uses `Codacy` for static analysis.
Coverage reports are generated and can be viewed in the Codacy dashboard.
Those are calculated only on the basis of the unit tests.

## Pipelines

The project uses GitHub Actions for continuous integration and deployment.
The coverage.yml file defines the workflow for running unittests and generating coverage reports.
The e2e-tests.yml file defines the workflow for running end-to-end tests.
The integration-tests.yml file defines the workflow for running integration tests.
the docker-image.yml file defines the workflow for building and pushing the Docker image to the GitHub Container Registry. (Only executed on the main branch)
