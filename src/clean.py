import shutil
from pathlib import Path
from pathlib import Path
from src.data import DATA_DIR
from src.utils.io import read_json
from loguru import logger
from typing import Union

class OrganiseFiles:
    """
    This class is used to organise files in a directory by
    moving files into directories based on  .
    """

    def __init__(self):
        ext_dirs = read_json(DATA_DIR / "extensions.json")
        self.extensions_dest = {}
        for dir_name, ext_list in ext_dirs.items():
            for ext in ext_list:
                self.extensions_dest[ext] = dir_name

    def __call__(self, directory: Union[str, Path]):
        """ Organise files in a directory by moving them to
        sub directories based on extensions.
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"{directory} not found.")

        logger.info(f"Organising files in {directory}...")
        file_extensions = list()
        for file_path in directory.iterdir():
            #ignore directories
            if file_path.is_dir():
                continue

            # ignore hidden files
            if file_path.name.startswith("."):
                continue

            # move files
            file_extensions.append(file_path.suffix)
            if file_path.suffix not in self.extensions_dest:
                DEST_DIR = directory / "other"
            else:
                DEST_DIR = directory / self.extensions_dest[file_path.suffix]

            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f"Moving {file_path} to {DEST_DIR}...")
            shutil.move(file_path, DEST_DIR)

if __name__ == "__main__":
    org_files = OrganiseFiles()
    org_files("/mnt/d/Downloads")
    logger.info("Done!")
