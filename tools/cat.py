'''File Reading function'''
from tools.path_utils import is_path_safe


def cat(path):
    '''
    Opens a file and reads its contents.

    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory(dir=".") as folder:
    ...     test = Path(folder).name + "/cars.txt"
    ...     _ = Path(test).write_text("Toyota", encoding="utf-8")
    ...     cat(test)
    'Toyota'

    >>> cat("file_no_exist.txt")
    'Cannot read file'

    >>> cat("../secret.txt")
    'Cannot read file'

    >>> with TemporaryDirectory(dir=".") as folder:
    ...     test = Path(folder) / "invalid.txt"
    ...     _ = test.write_bytes(b"\\xff")
    ...     cat(test)
    'Cannot read file'
    '''

    if is_path_safe(path) is False:
        return "Cannot read file"
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except (FileNotFoundError, UnicodeDecodeError):
        return "Cannot read file"
