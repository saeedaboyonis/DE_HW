import pytest
import os
from src.dags.de_hw_tasks import (
    list_files,
    download_file,
    validate_file,
    clean_data,
    check_flag,
    modify_file_branch1,
    modify_file_branch2,
    upload_file_to_gcs,
)
from src.dags.de_hw_utils import TEMPORARY_FOLDER_PATH


@pytest.fixture
def mock_gcs_list():
    return ["file1.json", "file2.json"]


@pytest.fixture
def mock_temp_folder():
    return "temp_folder"


@pytest.fixture
def mock_file_content():
    return {"id": 1, "name": "test", "flag": "branch1", "data": []}


@pytest.fixture
def mock_invalid_file_content():
    return {"id": "not_an_integer", "name": "test", "flag": "branch1", "data": []}


def test_list_files(mocker, mock_gcs_list):
    mocker.patch('src.dags.de_hw_tasks.GCSListObjectsOperator.execute', return_value=mock_gcs_list)
    files = list_files()
    assert files == mock_gcs_list


def test_download_file(mocker, mock_temp_folder):
    mocker.patch('src.dags.de_hw_tasks.GCSToLocalFilesystemOperator.execute')
    file_path = download_file("file1.json", mock_temp_folder)
    assert os.path.exists(file_path)


def test_validate_file(mocker, mock_file_content):
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(mock_file_content)))
    file_path = "temp_folder/file1.json"
    validated_file_path = validate_file(file_path)
    assert validated_file_path == file_path


def test_clean_data(mocker, mock_file_content):
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(mock_file_content)))
    file_path = "temp_folder/file1.json"
    cleaned_file_path = clean_data(file_path)
    assert cleaned_file_path == file_path


def test_clean_data_invalid(mocker, mock_invalid_file_content):
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(mock_invalid_file_content)))
    file_path = "temp_folder/file1.json"
    with pytest.raises(Exception):
        clean_data(file_path)


def test_check_flag(mocker, mock_file_content):
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(mock_file_content)))
    file_path = "temp_folder/file1.json"
    result = check_flag(file_path)
    assert result['branch'] == 'branch1'
    assert result['file_path'] == file_path


def test_modify_file_branch1(mocker, mock_file_content):
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(mock_file_content)))
    file_info = {'branch': 'branch1', 'file_path': "temp_folder/file1.json"}
    modified_file_path = modify_file_branch1(file_info)
    assert modified_file_path == file_info['file_path']


def test_modify_file_branch2(mocker, mock_file_content):
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(mock_file_content)))
    file_info = {'branch': 'branch2', 'file_path': "temp_folder/file1.json"}
    modified_file_path = modify_file_branch2(file_info)
    assert modified_file_path == file_info['file_path']


def test_upload_file_to_gcs(mocker, mock_temp_folder):
    mocker.patch('os.walk', return_value=[(TEMPORARY_FOLDER_PATH, [], ["file1.json"])])
    mocker.patch('src.dags.de_hw_tasks.LocalFilesystemToGCSOperator.execute')
    upload_file_to_gcs(mock_temp_folder)
