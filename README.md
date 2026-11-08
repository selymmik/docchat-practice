# Emperor Palpatine as your personal assistant
This program allows you to access 'openai/gpt-oss-20b' via your terminal by inputting chat.
Ensure that all dependencies are installed before operating. Note that the bot will respond in the tone and voice of Emperor Palpatine. The tool uses a Groq API to utilize four tool functions: calculate, grep, ls, and cat. Calculate executes when prompted with math problems, grep when asked to find a string within a file, ls when desiring to list the files and cat, to read files directly. All of these will be automatically called based on the context of a user's input. They can also be called manually by starting your prompt with /tool [parameter] (ex: /calculate 12*12).

PASTE INTO BASH TERMINAL:
``` bash
python -m build
python -m pip install .
chat
```

Examples of chatbot executing tasks on test_projects:
``` bash
chat> What files are inside test_projects/ebay-scraper?
```
``` text
Behold the contents of the *ebay‑scraper* domain:

- `README.md`
- `claremont mckenna.csv`
- `claremont mckenna.json`
- `drill press.csv`
- `drill press.json`
- `ebay-dl.py`
- `garden tools.csv`
- `garden tools.json`
- `practice-pages` (a directory)
- `practice-pages.zip`
- `submission.toml`
- `test.py`

The darkness of the file tree is now illuminated.
```

``` bash
chat> Show me the contents of test_projects/lab-homepage/README.md
```
``` text
# lab-homepage

Starter files for the **Hello, Homepage** and **Dress It Up** labs in *CSCI 40: Computing for the Web*.

- [Hello, Homepage](https://csci40.rtealwitter.com/topics/00_html/lab.html)
- [Dress It Up](https://csci40.rtealwitter.com/topics/01_css/lab.html)
- [Completed project](https://selymmik.github.io/lab-homepage/index.html)

May the light of knowledge guide you.
```

``` bash
chat> Find all lines containing "=" in test_projects/markdown-compiler/pyproject.toml
```
``` text
Here are the lines from `test_projects/markdown-compiler/pyproject.toml` that contain the character “=”:  


requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
name = "markdown_compiler"
version = "0.1.0"
description = "A markdown compiler"
requires-python = ">=3.8"
include = ["markdown_compiler*"]
markdown-compiler = "markdown_compiler.__main__:main"

May the knowledge you seek be yours.
```