#!/bin/bash
if [ ! -f .env ]; then
  echo "SHARED_PASSWORD=$(openssl rand -base64 32)" > .env
  echo ".env created with random password."
fi

docker-compose --env-file .env up
