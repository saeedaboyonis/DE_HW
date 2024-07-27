#!/usr/bin/env bash

# Define necessary directories
directories=("data" "logs" "src/plugins", "data/temporary")

# Define the environment variables
ENV_FILE=".env.local.user"
GCP_PROJECT_ID="seetree-proto-dev"
GCP_CREDENTIALS="/opt/airflow/credentials/seetree-proto-dev-8ec55e2c12e4.json"

# Clean up previous instances if needed and create necessary directories
for dir in "${directories[@]}"; do
    sudo rm -rf ./$dir
    [ ! -d ./$dir ] && sudo mkdir -p ./$dir && sudo chmod -R 0777 ./$dir
done

# Ensure environment file exists and is correct
if [ ! -f $ENV_FILE ]; then
    echo "AIRFLOW_UID=$(id -u)" > $ENV_FILE
else
    grep -q "AIRFLOW_UID=$(id -u)" $ENV_FILE || echo "AIRFLOW_UID=$(id -u)" > $ENV_FILE
fi

# Launch airflow initialization with Docker
docker compose --env-file "$ENV_FILE" up -d airflow-init

docker compose --env-file "$ENV_FILE" up -d airflow-webserver

echo "Wait for Airflow webserver to be up and running"
until $(curl --output /dev/null --silent --head --fail http://localhost:8080); do
    printf '.'
    sleep 2
done

echo "Add GCS connection inside the Docker container"
docker exec -it $(docker ps -qf "name=airflow-webserver") bash -c "
    airflow connections add 'de_hw' \
        --conn-type 'google_cloud_platform' \
        --conn-extra '{\"extra__google_cloud_platform__project\": \"'$GCP_PROJECT_ID'\", \"extra__google_cloud_platform__key_path\": \"'$GCP_CREDENTIALS'\"}'
"
echo "Add variables inside the Docker container"
docker exec -it $(docker ps -qf "name=airflow-webserver") bash -c "
    airflow variables import '/opt/airflow/vars.json'
"