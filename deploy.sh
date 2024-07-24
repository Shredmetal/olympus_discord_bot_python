#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Print each command before executing it (useful for debugging)
set -x

# Set environment variables
export DISCORD_BOT_TOKEN="your-bot-token"
export TROUBLESHOOTING_CHANNEL_ID="your-troubleshooting-channel-id"
export COMMUNITY_SUPPORT_CHANNEL_ID="your-community-support-channel-id"
export SUPPORT_REQUESTS_ID="your-support-requests-channel-id-for-bot-to-post-in"

# Build the Docker image
docker-compose build

# Stop and remove any existing container with the same name
docker-compose down

# Run the Docker container in detached mode
docker-compose up -d

# Print the status of the running containers
docker-compose ps