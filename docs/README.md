# DE_HW - Data Engineering Homework

![SeeTree Logo](../assets/seetree_logo.png)

## Project Overview

This project demonstrates a Data Engineering pipeline using Apache Airflow. The pipeline involves tasks such as downloading files from Google Cloud Storage (GCS), validating and cleaning JSON files, processing them based on specific flags, and uploading the processed files back to GCS.

## Project Structure
.
├── README.md
├── assets
│   └── seetree_logo.png
├── credentials
│   └── # service_account json files
├── data
│   └── temporary
├── docker-compose.yml
├── docs
│   └── README.md
├── logs
├── makefile
├── makefiles
│   ├── local.init.sh
│   ├── local.mk
│   ├── local.rebuild.sh
│   ├── local.start.sh
│   └── local.stop.sh
├── pyproject.toml
├── requirements.txt
├── src
│   ├── dags
│   │   ├── de_hw_task.py
│   │   ├── de_hw_tasks.py
│   │   ├── de_hw_utils.py
│   │   └── operators
│   │       ├── create_temp_folder_operator.py
│   │       └── remove_folder_operator.py
│   └── plugins
├── tests
└── vars.json

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose
- Python 3.7+

### Initial Setup

1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2. **Set up Google Cloud credentials:**
    - Place your GCS service account JSON file in the `credentials` folder.
    - Ensure the file is named `seetree-proto-dev-8ec55e2c12e4.json`.

3. **Configure environment variables:**
    - In `makefiles/local.init.sh`, set the following:
        ```sh
        GCP_PROJECT_ID="seetree-proto-dev"
        GCP_CREDENTIALS="/opt/airflow/credentials/seetree-proto-dev-8ec55e2c12e4.json"
        ```

4. **Initialize the project:**
    ```bash
    make init
    ```

    This will:
    - Create necessary directories.
    - Set permissions.
    - Initialize the Airflow environment with Docker.
    - Import variables from `vars.json` into Airflow.

5. **Start Airflow:**
    ```bash
    make start
    ```

    This will start all the necessary services in detached mode.

6. **Access Airflow UI:**
    - Open your browser and navigate to `http://localhost:8080`.
    - You can monitor the DAG runs, tasks, and logs here.

7. **Stop Airflow or Rebuild:**
    ```bash
    make start
    make rebuld
    ```

## Project Details

### DAG Definition

The main DAG (`de_hw_dag`) performs the following steps:

1. **Create Temporary Folder:**
    - A temporary folder is created to store the downloaded files.

2. **List Files:**
    - Lists files in a specified GCS bucket.

3. **Download Files:**
    - Downloads the listed files to the temporary folder.

4. **Validate Files:**
    - Validates the JSON files against a predefined schema.

5. **Clean Data:**
    - Cleans the JSON data based on the schema.

6. **Check Flag:**
    - Checks the `flag` in the JSON files to determine the processing branch.

7. **Modify Files:**
    - Modifies the files based on their respective branches (`branch1` and `branch2`).

8. **Upload Files:**
    - Uploads all modified files back to the GCS bucket.

### Code Organization

- **`dag.py`:** Contains the DAG definition.
- **`tasks.py`:** Contains task definitions for the DAG.
- **`utils.py`:** Contains utility functions and constants used across the project.
- **`operators`:** Custom operators for specific tasks.

### Environment Variables

The following environment variables are used in the project:

- `AIRFLOW_UID`: User ID for Airflow.
- `GCP_PROJECT_ID`: Google Cloud Project ID.
- `GCP_CREDENTIALS`: Path to the GCP credentials JSON file.

### vars.json

The `vars.json` file contains the variables that will be automatically imported into Airflow. You can configure it according to your requirements.

```json
{
    "de_hw_bucket_name": "your-bucket-name",
    "de_hw_connection_id": "your-connection-id",
    "STORAGE_ROOT_PATH": "/opt/airflow/data",
    "TEMPORARY_FOLDER_PATH": "temporary"
}
```

## Makefile Commands

The project uses a `makefile` for various tasks. Here are the available commands:

- **help**: Display help text.
- **start**: Start all services in detached mode.
- **stop**: Stop all services and remove containers.
- **init**: Initialize the environment, create directories, set permissions, and start Airflow initialization.
- **rebuild**: Rebuild the environment, recreate and rebuild all services.
- **create-dirs**: Create required directories for the project.
- **set-permissions**: Set proper permissions for project directories.

```bash
    make help
```

## Acknowledgements

- [Apache Airflow](https://airflow.apache.org/)
- [Google Cloud Platform](https://cloud.google.com/)
- [Docker](https://www.docker.com/)
