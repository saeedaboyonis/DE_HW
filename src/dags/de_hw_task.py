from airflow.decorators import dag
from de_hw_tasks import (
    create_temp_folder,
    list_files,
    download_file,
    validate_file,
    clean_data,
    check_flag,
    modify_file_branch1,
    modify_file_branch2,
    upload_file_to_gcs,
)
from de_hw_utils import default_args


@dag(
    default_args=default_args,
    catchup=False,
    description='A sample DAG for GCS data processing',
    schedule_interval="@once",
    tags=["gcs", "data processing"],
)
def de_hw_dag() -> None:
    """
    Define the DAG for GCS data processing.

    This DAG performs the following steps:
    1. Create a temporary folder.
    2. List files in a GCS bucket.
    3. Download files to the temporary folder.
    4. Validate the JSON files.
    5. Clean the JSON files based on a predefined schema.
    6. Check the 'flag' in the JSON files to determine the processing branch.
    7. Modify the files based on their respective branches.
    8. Upload all modified files back to the GCS bucket.

    Raises
    ------
    Exception
        If there is an error in any of the tasks.
    """
    temp_folder = create_temp_folder()
    files = list_files()

    download_tasks = download_file.partial(temp_folder=temp_folder).expand(file=files)
    validate_tasks = validate_file.expand(file_path=download_tasks)
    clean_tasks = clean_data.expand(file_path=validate_tasks)

    check_flags = check_flag.expand(file_path=clean_tasks)

    modify_file_branch1_task = modify_file_branch1.partial().expand(file_info=check_flags)
    modify_file_branch2_task = modify_file_branch2.partial().expand(file_info=check_flags)

    upload_task = upload_file_to_gcs(temp_folder=temp_folder)

    clean_tasks >> check_flags
    check_flags >> [modify_file_branch1_task, modify_file_branch2_task] >> upload_task


dag = de_hw_dag()
