'''Returning list of files when prompted'''
import glob
import os
from tools.path_utils import is_path_safe


def ls(path='.'):
    '''
    Returns a sorted list of files in a directory.

    >>> from pathlib import Path
    >>> folder = Path("test_ls_folder")
    >>> folder.mkdir()
    >>> _ = (folder / "apple.txt").write_text("Apple")
    >>> _ = (folder / "banana.txt").write_text("Banana")
    >>> [os.path.basename(p) for p in ls("test_ls_folder")]
    ['apple.txt', 'banana.txt']
    >>> (folder / "apple.txt").unlink()
    >>> (folder / "banana.txt").unlink()
    >>> folder.rmdir()
    >>> ls("../secret_files")
    'Cannot access directory outside of current'
    '''

    if is_path_safe(path) is False:
        return "Cannot access directory outside of current"
    files = glob.glob(os.path.join(path, '*'))
    return sorted(files)
