#!/bin/bash

# Exit script on error
set -e

# Define variables
IMAGE_NAME="votee-wordle-solver"
CONTAINER_NAME="votee-wordle-solver"

# Check if the first argument is '--build'
BUILD_IMAGE=false
if [ "$1" == "--build" ]; then
    BUILD_IMAGE=true
    shift # Remove the '--build' argument from the list
fi

# Step 1: Build the Docker image (if flagged)
if [ "$BUILD_IMAGE" = true ]; then
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME .
else
    echo "Skipping Docker image build..."
fi

# Step 2: Run the Docker container
echo "Running Docker container..."
docker run \
    --rm \
    --name $CONTAINER_NAME \
    --interactive \
    --volume $CONTAINER_NAME:/app \
    --tty \
    $IMAGE_NAME "$@"
