import logging
import os
from pathlib import Path

from airflow.models import BaseOperator


class RemoveFolderOperator(BaseOperator):
    template_fields = ['folder_path']

    def __init__(self, folder_path: str, *args, **kwargs):
        self.folder_path = folder_path
        super().__init__(*args, **kwargs)

    def execute(self, context):
        logging.info(self.folder_path)

        if os.path.isdir(self.folder_path):
            self._delete_folder(Path(self.folder_path))

    def _delete_folder(self, path) -> None:
        '''The function `_delete_folder` recursively deletes all files and subfolders within a given directory
        path.

        Parameters
        ----------
        pth
            The `pth` parameter in the `_delete_folder` method represents a Path object that points to a
        directory that needs to be deleted. The method recursively deletes all files and subdirectories
        within the specified directory before removing the directory itself.

        '''
        for sub in path.iterdir():
            if sub.is_dir():
                self._delete_folder(sub)
            else:
                sub.unlink()
        path.rmdir()
