#!/usr/bin/env bash

# Set script to exit immediately if any commands fail
set -e
# Define the environment file
ENV_FILE=".env.local.user"

# Print the action being taken
echo "Rebuilding and restarting the Docker containers with the new configuration..."

# Run docker-compose with the environment file
docker compose --env-file "$ENV_FILE" up --force-recreate --build -d

# Confirmation message
echo "Rebuild complete. Docker containers have been restarted."