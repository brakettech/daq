import pathlib
import re
import hug
import subprocess
import os
import textwrap

PWD = pathlib.Path(__file__).parent.resolve()
PROJ_PATH = PWD.parent.resolve()
VERSION_FILE = PWD.joinpath('__init__.py').resolve()
SCRIPT_FILE = PWD.joinpath('scripts.sh').resolve()
SERVER_PROJECT_PATH = pathlib.Path(os.path.expanduser('~/daq_server'))


def run(cmd, echo=True, dry_run=False):
    if echo:
        print(cmd)

    if not dry_run:
        os.system(cmd)


@hug.cli()
def version():
    with open(VERSION_FILE) as in_file:
        version_file_contents = in_file.read()
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file_contents, re.M)
    if version_match:
        print('braket-daq=={}'.format(version_match.group(1)))


@hug.cli()
def cd():
    run(f'cd {SERVER_PROJECT_PATH}')


@hug.cli()
def infect():
    commands = [
        'rm ~/.bashrc',
        f'cat ~/dot_files/.bashrc {SCRIPT_FILE} > ~/.bashrc',
    ]
    for cmd in commands:
        run(cmd)

    print('\n\n')
    print('Run this command to complete infection:  . ~/.bashrc')
    print()

@hug.cli()
def update():
    run('pip install -U braket-daq')

