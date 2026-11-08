''' Command F function'''

import glob
import re
from tools.path_utils import is_path_safe


def grep(regex, path):
    ''' Takes a regex and file path, opens that file and parses through lines
    that match initial regex query and outputs into a new list
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory(dir=".") as folder:
    ...     testing = Path(Path(folder).name)
    ...     test = Path(folder) / "test_cars.txt"
    ...     test2 = Path(folder) / "test_cars2.txt"
    ...     _ = test.write_text("the car is new\\nthe car is cool\\nCars 2 is great\\n")
    ...     _ = test2.write_text("the car is FABULOUS\\nthe car is FUN\\nCars 2 sucks\\nTrucks are better\\n")
    ...     grep("car", str(testing / "*.txt"))
    ['the car is new\\n', 'the car is cool\\n', 'the car is FABULOUS\\n', 'the car is FUN\\n']
    >>> with TemporaryDirectory(dir=".") as folder:
    ...     test = Path(folder) / "invalid.txt"
    ...     _ = test.write_bytes(b"\\xff")
    ...     grep("car", str(Path(folder).name + "/invalid.txt"))
    'Cannot read directory or file'
    >>> grep("car", "../secret.txt")
    'Cannot read directory or file'
    '''
    output = []
    files = glob.glob(path)
    if is_path_safe(path) is False:
        return "Cannot read directory or file"

    try:
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    if re.search(regex, line):
                        output.append(line)

    except (OSError, UnicodeDecodeError):
        return "Cannot read directory or file"

    return output
