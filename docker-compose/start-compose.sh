#!/bin/bash
if [ ! -f .env ]; then
  echo "SHARED_PASSWORD=$(openssl rand -base64 32)" > .env
  echo ".env created with random password."
fi

# Check if -d flag was passed
if [[ "$*" == *"-d"* ]]; then
  docker-compose --env-file .env up -d
else
  docker-compose --env-file .env up
fi