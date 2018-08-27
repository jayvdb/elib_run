# coding=utf-8
# coding=utf-8
"""
Finds an executable on the system
"""

import os
import sys
import typing
from pathlib import Path

from ._output import cmd_end, cmd_start

_KNOWN_EXECUTABLES = {}


def find_executable(executable: str, *paths: str) -> typing.Optional[Path]:  # noqa: C901
    # noinspection SpellCheckingInspection
    """
    Based on: https://gist.github.com/4368898

    Public domain code by anatoly techtonik <techtonik@gmail.com>

    Programmatic equivalent to Linux `which` and Windows `where`

    Find if ´executable´ can be run. Looks for it in 'path'
    (string that lists directories separated by 'os.pathsep';
    defaults to os.environ['PATH']). Checks for all executable
    extensions. Returns full path or None if no command is found.

    Args:
        executable: executable name to look for
        paths: root paths to examine (defaults to system PATH)

    Returns: executable path as string or None

    """

    if not executable.endswith('.exe'):
        executable = f'{executable}.exe'

    if executable in _KNOWN_EXECUTABLES:
        return _KNOWN_EXECUTABLES[executable]

    cmd_start(f'Looking for executable: {executable}')

    if not paths:
        path = os.environ['PATH']
        paths = tuple([str(Path(sys.exec_prefix, 'Scripts').absolute())] + path.split(os.pathsep))
    executable_path = Path(executable).absolute()
    if not executable_path.is_file():
        for path_ in paths:
            executable_path = Path(path_, executable).absolute()
            if executable_path.is_file():
                break
        else:
            cmd_end(f' -> not found')
            return None

    _KNOWN_EXECUTABLES[executable] = executable_path
    cmd_end(f' -> {str(executable_path)}')
    return executable_path
