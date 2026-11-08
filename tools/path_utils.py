'''Helper function to limit llm's ability to read folders and files to what is requested'''

from pathlib import PureWindowsPath


def is_path_safe(path):
    """
    Check whether a path is safe to access.

    >>> is_path_safe("test_cars.txt")
    True
    >>> is_path_safe("C:/Users/file.txt")
    False
    >>> is_path_safe("../secret.txt")
    False
    >>> is_path_safe("test_projects/ebay-scraper")
    True
    """
    path = str(path)

    if PureWindowsPath(path).is_absolute():
        return False

    if ".." in path:
        return False

    return True
