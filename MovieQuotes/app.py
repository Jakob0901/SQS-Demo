import logging
import os
from flask import Flask, request, jsonify, render_template
from functools import wraps
from flask_wtf.csrf import CSRFProtect

from wrapper.QuotesApi import QuotesApi
from database.Storage import Storage

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
        self.app.config['WTF_CSRF_ENABLED'] = True
        self.csrf = CSRFProtect(self.app)

        self.quotes_api_wrapper = QuotesApi()
        self.API_KEY = os.environ.get('API_KEY')
        self.db = None  # Platzhalter für Unitests; regulär wird er in der Funktion initialize_database() initialisiert

        self.initialize_database()

        self.app.route('/')(self.get_index)
        self.app.route('/quote')(self.get_quote)
        self.app.route('/stored_quotes')(self.require_api_key(self.get_stored_quotes))
        self.app.route('/save', methods=['POST'])(self.require_api_key(self.save_quote))

    def initialize_database(self):
        if os.environ.get('FLASK_ENV') != 'testing':
            database_url = os.environ.get('DATABASE_URL', 'localhost:5432')
            username = os.environ.get('DB_USERNAME', 'username')
            password = os.environ.get('DB_PASSWORD', 'password')
            self.db = Storage(database_url, username, password)

    def require_api_key(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.headers.get('x-api-key') == self.API_KEY:
                return f(*args, **kwargs)
            else:
                return jsonify({"message": "Forbidden"}), 403
        return decorated_function

    def get_index(self):
        return render_template('index.html')

    def get_quote(self):
        return self.quotes_api_wrapper.get_random_quote()

    def get_stored_quotes(self):
        return self.db.get_all_quotes() if self.db else jsonify([])

    def save_quote(self):
        data = request.form.get('quote')
        logging.info(data)
        if not data:
            return jsonify({"message": "No quote provided"}), 400
        else:
            if self.db:
                self.db.store_quote(data)
                logging.info("Quote saved to database")
            return jsonify({"message": "Quote saved!"}), 200

    def run(self):
        if not self.API_KEY:
            raise ValueError("No API_KEY environment variable set")
        self.app.run()

if __name__ == '__main__':
    flask_app = FlaskApp()
    flask_app.run()
