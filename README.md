# SQS-Demo (Simple Quote Service)

Ein Service zum Abrufen und Speichern von Zitaten, bestehend aus einer Python/Flask-Backend-API und Vue.js Frontend.

## Features

- Abrufen von zufälligen Zitaten
- Speichern von Lieblingszitaten
- RESTful API mit Rate-Limiting
- API-Key Authentifizierung

## Dokumentation

Die vollständige Dokumentation im arc42-Format ist verfügbar:

- In `/docs`
- Auf [Read the Docs](https://sqs-demo.readthedocs.io/)

## Voraussetzungen

- Docker & Docker Compose für Container-Ausführung
- Python 3.11 für lokale Entwicklung

## Quick Start

### Mit Docker

```bash
cd docker-compose
./start-compose.sh
```

### Lokale Entwicklung

Benötigte Umgebungsvariablen:

```env
PYTHONUNBUFFERED=1
API_KEY=secure
DB_USERNAME=user
DB_PASSWORD=kernschmelze
DATABASE_URL=localhost:5432/app_db
```

### Abhängigkeiten installieren

```bash
cd QuoteService
pip install .
```

Dieser Befehl installiert die Abhängigkeiten aus der `setup.py`.

### Datenbank initialisieren

```bash
cd QuoteService/tests
dokcker-compose up
```

Dieser Befehl startet die Testdatenbank. 
Dies wurde mit Docker Compose eingerichtet, wobei die docker-compose.yml die für Integrations und e2e Tests genutzt wird, im `tests`-Verzeichnis liegt.

### Start application

```bash
cd QuoteService
python3 app.py
```

This starts the Flask application on `http://localhost:80`.

## CI/CD

- Automatisierte Tests via GitHub Actions
- Docker Images verfügbar im GitHub Container Registry

## Lizenz

Dieses Projekt steht unter der [MIT Lizenz](LICENSE).

## Weitere Informationen

Das Projekt wird auf GitHub gehostet: [Jakob0901/SQS-Demo](https://github.com/Jakob0901/SQS-Demo).
Detaillierte Informationen zur Installation, API-Dokumentation und Architektur finden Sie in der [Dokumentation](https://sqs-demo.readthedocs.io/).
Das Projekt wird mithilfe von Codacy auf Code-Qualität geprüft und analysiert. Die Ergebnisse sind auf der [Codacy-Seite](https://app.codacy.com/gh/Jakob0901/SQS-Demo/dashboard/) einsehbar.
