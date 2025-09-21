#!/bin/bash
# Script to start up the Flask server inside of a container

# Set the Image name
IMAGE_NAME="itsandrewc/app"

# Find a dynamic port on the machine
for port in {5000..5100}; do
  if ! lsof -iTCP:$port -sTCP:LISTEN >/dev/null; then
    echo "FREE_PORT=$port" > .env
    break
  fi
done

# Run docker compose with the .env file
docker compose up
