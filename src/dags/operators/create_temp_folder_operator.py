import logging
import os
import random
import string
from pathlib import Path

from airflow.models import BaseOperator


class CreateTempFolderOperator(BaseOperator):

    def __init__(self, parent_folder: str, string_length: int = 10, *args, **kwargs):
        self.parent_folder = parent_folder
        self.string_length = string_length
        super(CreateTempFolderOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        logging.info(self.parent_folder)

        folder_name = ''.join(random.choice(string.ascii_letters) for i in range(self.string_length))
        string_path = os.path.join(self.parent_folder, folder_name)
        path = Path(string_path)
        path.mkdir(parents=True, exist_ok=True)
        logging.info(path.absolute())
        return folder_name
