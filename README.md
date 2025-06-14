```markdown
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

## CI/CD

- Automatisierte Tests via GitHub Actions
- Docker Images verfügbar im GitHub Container Registry

## Lizenz

Dieses Projekt steht unter der [MIT Lizenz](LICENSE).

## Weitere Informationen

Detaillierte Informationen zur Installation, API-Dokumentation und Architektur finden Sie in der [Dokumentation](https://sqs-demo.readthedocs.io/).
```