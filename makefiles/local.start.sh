#!/usr/bin/env bash

# Set script to exit immediately if any commands fail
set -e

# Define the environment file
ENV_FILE=".env.local.user"

# Print action being taken
echo "Starting the Docker containers..."

# Start Docker containers with the specified environment file
docker compose --env-file "$ENV_FILE" up -d

# Confirmation message
echo "Docker containers are up and running."