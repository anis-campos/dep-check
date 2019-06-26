"""
Implementation of configuration reader and writer
"""
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from dep_check.models import Module, SourceCode, SourceFile


def _get_module_from_file_path(path: Path) -> Module:
    """
    Transform a filename into a corresponding python module.
    """
    path_without_extention = path.parents[0] / path.stem
    return Module(".".join(path_without_extention.parts))


@contextmanager
def _change_dir(directory: str) -> Iterator[None]:
    """
    Locally change current working directory
    """
    saved_dir = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(saved_dir)


def source_file_iterator(root_dir: str) -> Iterator[SourceFile]:
    """
    Iterator of all python source files in a directory.
    """
    with _change_dir(root_dir):
        for file_path in Path(".").rglob("*.py"):
            with open(str(file_path), "r") as stream:
                content = stream.read()
            yield SourceFile(_get_module_from_file_path(file_path), SourceCode(content))