FROM python:3.11-slim-bookworm

WORKDIR /app

# Passe den Pfad an, damit QuotesService korrekt kopiert wird
COPY ../QuotesService /app/QuotesService

WORKDIR /app/QuotesService

RUN pip install --no-cache-dir .

EXPOSE 80

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh ./wait-for-it.sh
RUN chmod +x ./wait-for-it.sh

CMD ./wait-for-it.sh localhost:5432 -- python3 app.py