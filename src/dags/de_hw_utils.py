import os
import json
import logging
from datetime import timedelta
from airflow.models import Variable
from airflow.utils.dates import days_ago

DAG_ID = "DE_HW"
BUCKET_NAME = Variable.get('de_hw_bucket_name')
GCP_CONNECTION_ID = Variable.get('de_hw_connection_id')
TEMPORARY_FOLDER_PATH = os.path.join(
    Variable.get('STORAGE_ROOT_PATH'), Variable.get('TEMPORARY_FOLDER_PATH').lstrip('/')
)

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

json_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "flag": {"type": "string"},
        "data": {"type": "array", "items": {"type": "object"}},
    },
    "required": ["id", "name", "flag", "data"],
}

logger = logging.getLogger(__name__)


def sanitize_task_id(task_id: str) -> str:
    """
    Sanitize a task ID by removing invalid characters.

    Parameters
    ----------
    task_id : str
        The original task ID.

    Returns
    -------
    str
        The sanitized task ID.
    """
    return ''.join(e for e in task_id if e.isalnum() or e == '_')


def modify_file(file_path: str, modification: str) -> str:
    """
    Modify the JSON file by adding a modification flag.

    Parameters
    ----------
    file_path : str
        The path of the file to modify.
    modification : str
        The modification flag to add to the file.

    Returns
    -------
    str
        The path of the modified file.

    Raises
    ------
    Exception
        If there is an error reading, modifying, or writing the file.
    """
    try:
        logging.info(f"Running modification for {file_path} with modification: {modification}")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        data['modified'] = modification
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file)
        return file_path
    except Exception as e:
        logger.error(f"Error modifying file {file_path}: {e}")
        raise
