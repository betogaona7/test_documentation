"""@DEVTALE-GENERATED: This script is a command-line tool that fuses documentation into code
from various languages including Python, PHP, Go, and Javascript. It takes several
command-line arguments including the path to the file or directory, an output path for the
documentation, and the name of the OpenAI model to use. It also supports recursive
exploration of subdirectories, docstring insertion into code files, and debug mode.
"""

import copy
import getpass
import json
import logging
import os

import click
from dotenv import load_dotenv

from devtale.aggregators import (
    GoAggregator,
    JavascriptAggregator,
    PHPAggregator,
    PythonAggregator,
)
from devtale.constants import ALLOWED_EXTENSIONS, LANGUAGES
from devtale.utils import (
    build_project_tree,
    extract_code_elements,
    fuse_tales,
    get_unit_tale,
    prepare_code_elements,
    redact_tale_information,
    split_code,
    split_text,
)

DEFAULT_OUTPUT_PATH = "devtale_demo/"
DEFAULT_MODEL_NAME = "gpt-4"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fuse_documentation(code, tale, output_path, file_name, file_ext):
    """@DEVTALE-GENERATED: This method fuses the generated documentation with the corresponding
    code. Args: code (str): The source code to document. tale (str): The generated
    documentation. output_path (str): The path where the documented code will be saved.
    file_name (str): The name of the file. file_ext (str): The extension of the file."""
    save_path = os.path.join(output_path, file_name)
    logger.info(f"save fused dev tale in: {save_path}")

    if file_ext == ".py":
        aggregator = PythonAggregator()
    elif file_ext == ".php":
        aggregator = PHPAggregator()
    elif file_ext == ".go":
        aggregator = GoAggregator()
    elif file_ext == ".js":
        aggregator = JavascriptAggregator()

    fused_tale = aggregator.document(code=code, documentation=tale)
    with open(save_path, "w") as file:
        file.write(fused_tale)


@click.command()
@click.option(
    "-p",
    "--path",
    "path",
    required=True,
    help="The path to the repository, folder, or file",
)
@click.option(
    "-r",
    "--recursive",
    "recursive",
    is_flag=True,
    default=False,
    help="Allows to explore subfolders.",
)
@click.option(
    "-f",
    "--fuse",
    "fuse",
    is_flag=True,
    default=False,
    help="Adds the docstrings inside the code file.",
)
@click.option(
    "-o",
    "--output-path",
    "output_path",
    required=False,
    default=DEFAULT_OUTPUT_PATH,
    help="The destination folder where you want to save the documentation outputs",
)
@click.option(
    "-n",
    "--model-name",
    "model_name",
    required=False,
    default=DEFAULT_MODEL_NAME,
    help="The OpenAI model name you want to use. \
    https://platform.openai.com/docs/models",
)
@click.option(
    "--debug",
    "debug",
    is_flag=True,
    default=False,
    help="Mock answer and avoid GPT calls",
)
def main(
    path: str,
    recursive: bool,
    fuse: bool,
    output_path: str = DEFAULT_OUTPUT_PATH,
    model_name: str = DEFAULT_MODEL_NAME,
    debug: bool = False,
):
    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass(
            prompt="Enter your OpenAI API key: "
        )

if __name__ == "__main__":
    main()
