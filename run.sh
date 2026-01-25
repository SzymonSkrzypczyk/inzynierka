#!/bin/bash

MAX_RETRIES=3
RETRY_DELAY=10
SERVICE_DASHBOARD="dashboard"

if [ ! -f .env ]; then
    echo "No .env file found. Please create one."
    exit 1
fi

echo "Starting project deployment..."

run_pipeline() {
    echo "Running data pipeline (collect-data -> save-database)..."
    docker-compose up --exit-code-from save-database save-database
    return $?
}

attempt=1
while [ $attempt -le $MAX_RETRIES ]; do
    echo "Attempt $attempt of $MAX_RETRIES..."
    
    run_pipeline
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "Data pipeline completed successfully."
        break
    else
        echo "Pipeline failed with exit code $exit_code."
        if [ $attempt -lt $MAX_RETRIES ]; then
            echo "Retrying in $RETRY_DELAY seconds..."
            sleep $RETRY_DELAY
            attempt=$((attempt + 1))
        else
            echo "Max retries reached. Exiting."
            exit 1
        fi
    fi
done

echo "Starting Dashboard..."
docker-compose up -d $SERVICE_DASHBOARD

if [ $? -eq 0 ]; then
    echo "Dashboard is running at http://localhost:8501"
else
    echo "Failed to start dashboard."
    exit 1
fi
