import os
from flask import Flask, request, jsonify, render_template
from functools import wraps
from flask_wtf.csrf import CSRFProtect

from wrapper.QuotesApi import QuotesApi

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['WTF_CSRF_ENABLED'] = True
csrf = CSRFProtect(app)

quotes_api_wrapper = QuotesApi()

API_KEY = os.environ.get('API_KEY')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') == API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Forbidden"}), 403

    return decorated_function

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/quote')
def get_quote():
    return quotes_api_wrapper.get_random_quote()

@app.route('/stored_quotes')
@require_api_key
def get_stored_quotes():
    return "Quotes will be stored here!"

@app.route('/save', methods=['POST'])
@require_api_key
def save_quote():
    data = request.form.get('quote')
    print(data)
    return "Quote saved!"

if __name__ == '__main__':
    if not API_KEY:
        raise ValueError("No API_KEY environment variable set")

    app.run(ssl_context='adhoc')