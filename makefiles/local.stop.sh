#!/usr/bin/env bash

# Set script to exit immediately if any commands fail
set -e

# Define the environment file
ENV_FILE=".env.local.user"

# Inform user about the action being taken
echo "Stopping and removing the Docker containers..."

# Stop and remove Docker containers using the specified environment file
docker compose --env-file "$ENV_FILE" down

# Confirmation message
echo "Docker containers have been stopped and removed."