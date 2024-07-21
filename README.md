![seetree](./assets/seetree_logo.png)

# Submission Deadline: Jul 20st, 2024

# Homework Exercise

#### Airflow DAG for JSON Processing Scenario
Create an Airflow DAG to fetch a JSON file from a GCP bucket, process it based on a flag, branch into different paths, modify the file differently in each branch, and upload the modified file back to the GCP bucket. Additionally, include steps for validating the JSON schema and cleaning the data, along with error handling, logging, and monitoring mechanisms.
#### Requirements
1. Fetch a JSON file from a GCP bucket.
2. Validate the JSON schema.
3. Clean the data.
4. Process the data based on a flag.
5. Branch into different paths based on the flag.
6. Modify the file differently in each branch.
7. Upload the modified file back to the GCP bucket.
8. Include error handling, logging, and monitoring mechanisms.

#### Detailed Steps
### Step 1: Fetch JSON File from GCP Bucket
Use the `GCSToLocalFilesystemOperator` to download the JSON file from a specified GCP bucket to the local filesystem.

### Step 2: Validate JSON Schema
Use the `PythonOperator` to validate the JSON file against a predefined schema. If the schema validation fails, the DAG should stop and log the error.

### Step 3: Clean Data
Use the `PythonOperator` to clean the data. This can include removing null values, correcting data formats, etc.

### Step 4: Process Data Based on Flag
Use the `BranchPythonOperator` to branch the workflow based on a flag in the JSON data. Define different paths for each flag value.


This function checks the flag value in the JSON data and directs the workflow to the appropriate branch.

### Step 5: Modify File in Each Branch
In each branch, use the `PythonOperator` to modify the JSON file as required. Each branch will have its own modification logic.

For example, in `modify_file_branch1`:

```python
def modify_file_branch1(**kwargs):
....
    # Modify data as needed for branch1
    data['modified'] = 'branch1_modification'
....  
```


Each branch function pulls the JSON data, applies the necessary modifications, and saves the modified data back to a file.

### Step 6: Upload Modified File Back to GCP Bucket
Use the `LocalFilesystemToGCSOperator` to upload the modified JSON file back to a specified GCP bucket.

### Step 7: Error Handling, Logging, and Monitoring
Implement error handling and logging in each step using try-except blocks and the `Airflow logging` module. Use Airflow's built-in monitoring tools to monitor the DAG execution.

Example JSON Schema
```
{
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "name": {"type": "string"},
    "flag": {"type": "string"},
    "data": {"type": "array", "items": {"type": "object"}}
  },
  "required": ["id", "name", "flag", "data"]
}
```

Sample JSON Data
```
{
  "id": 123,
  "name": "Sample Name",
  "flag": "branch1",
  "data": [
    {"key1": "value1"},
    {"key2": "value2"}
  ]
}
```

### Authenticating to Seetree Bucket

To connect to the Seetree bucket, follow these steps to authenticate using the provided secret credentials JSON file:

1. **Obtain Credentials:**
   - You will receive a JSON file containing your service account credentials via email.

2. **Authenticate with Google Cloud:**
   - Open a terminal and use the `gcloud` command-line tool to authenticate using the service account credentials. Run the following command:
     ```bash
     gcloud auth activate-service-account --key-file=path/to/your/credentials-file.json
     ```
   - Replace `path/to/your/credentials-file.json` with the path to the JSON file you received.

3. **Verify Authentication:**
   - Ensure that your authentication is successful by running:
     ```bash
     gcloud auth list
     ```
   - This should list the active account and indicate that the service account is in use.

4. **Access the Bucket:**
   - Use `gsutil` to read from or write to the Seetree bucket. For example, to copy a file from your local filesystem to the bucket, use:
     ```bash
     gsutil cp local-file.json gs://your-seetree-bucket/
     ```
   - To download a file from the bucket to your local filesystem, use:
     ```bash
     gsutil cp gs://your-seetree-bucket/remote-file.json local-file.json
     ```

   - Replace `your-seetree-bucket` with the name of the Seetree bucket.

These steps will set up authentication for accessing and managing files in the Seetree bucket.

#### Input
1. The workflow should be triggered by REST API POST request 
https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html
Example of POST request using curl:
```
> curl -X POST 'http://localhost:8080/api/v1/dags/<dag_id>/dagRuns' \
   	-H 'Content-Type: application/json' \
--user "airflow:airflow"
```
2. Example of successful response:
```
{"execution_date":"2020-11-11T18:45:05+00:00","message":"Created <DagRun test_dag @ 2020-11-11 18:45:05+00:00: manual__2020-11-11T18:45:05+00:00, externally triggered: True>"}
```


### Required Deliverables

1. Code implementing the algorithm you developed, in a programming language of your choice. 
on this repository, in the `src` directory (open a PR for submission).
    - The code should be well-documented and easy to read, and should include instructions for running the code.

3. A document describing the assumptions, approach, and results (including intermediate results of your choice):
   - Please dedicate no more than one page to describing the assumptions and solution approach.

   
#### Environment Setup Guide
1. Install Python 3.7 - https://www.python.org/downloads/release/python-370/
2. Python IDE of your choice (VS code is recommended https://code.visualstudio.com/download)
3. Install Docker Engine - https://docs.docker.com/desktop/
4. Install REST API tool of your choice (POSTMAN is recommended https://www.postman.com/downloads)
5. Follow this guide to initialize a local airflow instance: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#running-airflow-in-docker
6. Disable example dags by editing the docker-compose.yaml file or in any other way.
7. Go to http://localhost:8080/. You should be able to access the Airflow web application.


#### References
Apache Airflow - https://airflow.apache.org/docs/apache-airflow/2.5.1/tutorial/index.html
Docker logs for basic debugging -  https://docs.docker.com/config/containers/logging/
