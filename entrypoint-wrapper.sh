#!/bin/bash
# turn on bash's job control
set -m
# Start the dockerd daemon and put it in the background
dockerd-entrypoint.sh &
# Wait until the daemon comes up
while ! docker ps
do
echo "Waiting for docker daemon..."
sleep 2
done
# Run the containers
cd /app
echo "Docker daemon is up - executing command"
docker-compose up --build