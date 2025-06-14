import logging
import os
from flask import Flask, request, jsonify, render_template
from functools import wraps
from flask_wtf.csrf import CSRFProtect

from wrapper.QuotesApi import QuotesApi, QuoteServiceError
from database.Storage import Storage, DatabaseError

# Logger-Konfiguration
logger = logging.getLogger(__name__)


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = os.environ.get('API_KEY')
        if request.headers.get('x-api-key') == api_key:
            logger.debug("API-Key-Authentifizierung erfolgreich")
            return f(*args, **kwargs)
        else:
            logger.warning("Ungültiger API-Key-Versuch")
            return jsonify({"message": "Forbidden"}), 403

    return decorated_function


class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
        self.app.config['WTF_CSRF_ENABLED'] = True
        self.csrf = CSRFProtect(self.app)

        self.quotes_api_wrapper = QuotesApi()
        self.API_KEY = os.environ.get('API_KEY')
        self.db = None

        logger.info("FlaskApp wird initialisiert")
        self.initialize_database()
        self.initialize_routes()
        logger.info("FlaskApp erfolgreich initialisiert")

    def initialize_routes(self):
        logger.debug("Routen werden registriert")
        self.app.route('/')(self.get_index)
        self.app.route('/quote')(self.get_quote)
        self.app.route('/stored_quotes')(self.get_stored_quotes)
        self.app.route('/save', methods=['POST'])(self.save_quote)
        logger.debug("Routen erfolgreich registriert")

    def initialize_database(self):
        try:
            if os.environ.get('FLASK_ENV') != 'testing':
                database_url = os.environ.get('DATABASE_URL', 'localhost:5432/db')
                username = os.environ.get('DB_USERNAME', 'username')
                logger.info(f"Verbindung zur Datenbank wird hergestellt: {database_url}")
                self.db = Storage(database_url, username, os.environ.get('DB_PASSWORD', 'password'))
                logger.info("Datenbankverbindung erfolgreich hergestellt")
        except DatabaseError as e:
            logger.error("Datenbankinitialisierung fehlgeschlagen", exc_info=True)
            self.db = None

    def get_index(self):
        logger.debug("Index-Seite wird angefordert")
        return render_template('index.html')

    def get_quote(self):
        logger.debug("Zufälliges Zitat wird angefordert")
        try:
            quote = self.quotes_api_wrapper.get_random_quote()
            logger.debug("Zitat erfolgreich abgerufen")
            return quote
        except QuoteServiceError as e:
            logger.error("Fehler beim Abrufen des Zitats", exc_info=True)
            return jsonify({"error": "Interner Serverfehler"}), 500

    @require_api_key
    def get_stored_quotes(self):
        logger.debug("Gespeicherte Zitate werden abgerufen")
        return self.db.get_all_quotes() if self.db else jsonify([])

    @require_api_key
    def save_quote(self):
        data = request.form.get('quote')
        if not data:
            logger.warning("Versuch, leeres Zitat zu speichern")
            return jsonify({"message": "No quote provided"}), 400

        logger.debug(f"Speicheranfrage für Zitat erhalten: {data[:50]}...")

        if self.db:
            try:
                self.db.store_quote(data)
                logger.info("Zitat erfolgreich in Datenbank gespeichert")
                return jsonify({"message": "Quote saved!"}), 200
            except ValueError as e:
                logger.warning("Fehler leeres Zitat", exc_info=True)
                return jsonify({"error": str(e)}), 400
            except DatabaseError as e:
                logger.error("Fehler beim Speichern des Zitats", exc_info=True)
                return jsonify({"error": "Datenbankfehler"}), 500
        return jsonify({"message": "Quote saved!"}), 200

    def run(self):
        if not self.API_KEY:
            logger.critical("Kein API_KEY in Umgebungsvariablen gefunden")
            raise ValueError("No API_KEY environment variable set")
        logger.info("Server wird gestartet")
        self.app.run()