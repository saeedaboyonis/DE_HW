import json
from datetime import datetime
import logging
import os
from jsonschema import validate, ValidationError
from airflow.decorators import task
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from de_hw_utils import (
    BUCKET_NAME,
    GCP_CONNECTION_ID,
    TEMPORARY_FOLDER_PATH,
    json_schema,
    sanitize_task_id,
    modify_file,
)
from operators.create_temp_folder_operator import CreateTempFolderOperator

logger = logging.getLogger(__name__)


@task
def list_files(**kwargs) -> list:
    """
    List files in the specified GCS bucket.

    Parameters
    ----------
    kwargs : dict
        Additional keyword arguments.

    Returns
    -------
    list
        A list of file names in the specified GCS bucket.

    Raises
    ------
    Exception
        If there is an error listing files.
    """
    try:
        files = GCSListObjectsOperator(
            task_id='list_files',
            bucket=BUCKET_NAME,
            prefix='test',
            gcp_conn_id=GCP_CONNECTION_ID,
        ).execute(context=kwargs)
        return files
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise


@task
def create_temp_folder(**kwargs) -> str:
    """
    Create a temporary folder for storing files.

    Parameters
    ----------
    kwargs : dict
        Additional keyword arguments.

    Returns
    -------
    str
        Path of the created temporary folder.

    Raises
    ------
    Exception
        If there is an error creating the temporary folder.
    """
    try:
        temp_folder = CreateTempFolderOperator(
            task_id="create_temp_folder",
            parent_folder=TEMPORARY_FOLDER_PATH,
        ).execute(context=kwargs)
        return temp_folder
    except Exception as e:
        logger.error(f"Error creating temporary folder: {e}")
        raise


@task
def download_file(file: str, temp_folder: str, **kwargs) -> str:
    """
    Download a file from GCS to a local temporary folder.

    Parameters
    ----------
    file : str
        The name of the file to download.
    temp_folder : str
        The path of the temporary folder where the file will be downloaded.
    kwargs : dict
        Additional keyword arguments.

    Returns
    -------
    str
        The local path where the file has been downloaded.

    Raises
    ------
    Exception
        If there is an error downloading the file.
    """
    try:
        local_path = os.path.join(TEMPORARY_FOLDER_PATH, temp_folder, file)
        GCSToLocalFilesystemOperator(
            task_id=f'download_{sanitize_task_id(file)}',
            bucket=BUCKET_NAME,
            object_name=file,
            filename=local_path,
            gcp_conn_id=GCP_CONNECTION_ID,
        ).execute(context=kwargs)
        return local_path
    except Exception as e:
        logger.error(f"Error downloading file {file}: {e}")
        raise


@task
def validate_file(file_path: str, **kwargs) -> str:
    """
    Validate the JSON file against a predefined schema.

    Parameters
    ----------
    file_path : str
        The path of the file to validate.
    kwargs : dict
        Additional keyword arguments.

    Returns
    -------
    str
        The path of the validated file.

    Raises
    ------
    ValidationError
        If the JSON file does not conform to the schema.
    Exception
        If there is an error reading the file or validating its content.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        validate(instance=data, schema=json_schema)
        logging.info(f"JSON file {file_path} is valid.")
        return file_path
    except ValidationError as e:
        logger.error(f"JSON file {file_path} is invalid: {e.message}")
        raise
    except Exception as e:
        logger.error(f"Error validating file {file_path}: {e}")
        raise


@task
def clean_data(file_path: str, **kwargs) -> str:
    """
    Clean the JSON file data based on the predefined schema.

    Parameters
    ----------
    file_path : str
        The path of the file to clean.
    kwargs : dict
        Additional keyword arguments.

    Returns
    -------
    str
        The path of the cleaned file.

    Raises
    ------
    Exception
        If there is an error reading, cleaning, or writing the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Cleaning the data based on the schema
        cleaned_data = {}
        for key, value in data.items():
            if key in json_schema["properties"]:
                expected_type = json_schema["properties"][key]["type"]
                if expected_type == "array" and isinstance(value, list):
                    cleaned_data[key] = [item for item in value if isinstance(item, dict)]
                elif expected_type == "integer" and isinstance(value, int):
                    cleaned_data[key] = value
                elif expected_type == "string" and isinstance(value, str):
                    cleaned_data[key] = value
                else:
                    logging.warning(f"Type mismatch or invalid data for key: {key}")
            else:
                logging.warning(f"Unexpected key: {key}")

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(cleaned_data, file)
        return file_path
    except Exception as e:
        logger.error(f"Error cleaning data in file {file_path}: {e}")
        raise


@task
def modify_file_branch1(file_info: dict, **kwargs) -> str:
    """
    Modify the file for branch1.

    Parameters
    ----------
    file_info : dict
        Dictionary containing branch and file path information.
    kwargs : dict
        Additional keyword arguments.

    Returns
    -------
    str
        The path of the modified file.

    Raises
    ------
    Exception
        If there is an error modifying the file.
    """
    file_path = file_info['file_path']
    return modify_file(file_path, 'branch1_modification')


@task
def modify_file_branch2(file_info: dict, **kwargs) -> str:
    """
    Modify the file for branch2.

    Parameters
    ----------
    file_info : dict
        Dictionary containing branch and file path information.
    kwargs : dict
        Additional keyword arguments.

    Returns
    -------
    str
        The path of the modified file.

    Raises
    ------
    Exception
        If there is an error modifying the file.
    """
    file_path = file_info['file_path']
    return modify_file(file_path, 'branch2_modification')


@task
def upload_file_to_gcs(temp_folder: str, **kwargs) -> None:
    """
    Upload all files in the temporary folder to the GCS bucket.
    Parameters
    ----------
    temp_folder : str
        The path of the temporary folder containing files to upload.
    kwargs : dict
        Additional keyword arguments.

    Raises
    ------
    Exception
        If there is an error uploading the files.
    """
    try:
        local_path = os.path.join(TEMPORARY_FOLDER_PATH, temp_folder)
        logging.info(f'Uploading files from {local_path} to GCS bucket {BUCKET_NAME}')
        for root, dirs, files in os.walk(local_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_name, file_ext = os.path.splitext(os.path.basename(file_path))
                str_current_datetime = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
                new_file_name = f"updated_{file_name}_at_{str_current_datetime}{file_ext}"
                new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

                logging.info(f'Renaming {file_path} to {new_file_path}')
                os.rename(file_path, new_file_path)

                logging.info(f'Uploading file {new_file_path} to GCS bucket {BUCKET_NAME}')
                LocalFilesystemToGCSOperator(
                    task_id=f'upload_{sanitize_task_id(file_name)}',
                    src=new_file_path,
                    dst=new_file_name,
                    bucket=BUCKET_NAME,
                    gcp_conn_id=GCP_CONNECTION_ID,
                ).execute(context=kwargs)
    except Exception as e:
        logger.error(f"Error uploading files to GCS: {e}")
        raise


@task
def check_flag(file_path: str, **kwargs) -> dict:
    """
    Check the flag in the JSON file and return branch information.
    Parameters
    ----------
    file_path : str
        The path of the file to check.
    kwargs : dict
        Additional keyword arguments.

    Returns
    -------
    dict
        Dictionary containing branch and file path information.

    Raises
    ------
    ValueError
        If the flag is invalid or not found.
    Exception
        If there is an error reading the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if 'flag' in data:
            flag_value = data['flag']
            if flag_value == 'branch1':
                return {'branch': 'branch1', 'file_path': file_path}
            elif flag_value == 'branch2':
                return {'branch': 'branch2', 'file_path': file_path}
            else:
                raise ValueError('Invalid flag')
        else:
            raise ValueError("No 'flag' found in JSON data.")
    except Exception as e:
        logger.error(f"Error checking flag in file {file_path}: {e}")
        raise
