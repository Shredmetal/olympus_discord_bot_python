#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Print each command before executing it (useful for debugging)
set -x

# Build the Docker image
docker-compose build

# Stop and remove any existing container with the same name
docker-compose down

# Run the Docker container in detached mode
docker-compose up -d

# Print the status of the running containers
docker ps