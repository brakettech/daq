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


# @hug.cli()
# def server(port=None):
#     if port is None:
#         port = '8000'
#
#     print('\n\n')
#     print('-'*80)
#     print(f'Point your browser to http://localhost:{port}')
#     print('-'*80)
#     print('\n\n')
#
#
#     p = subprocess.Popen(['gunicorn', f'--pythonpath={PROJ_PATH}', 'daq.wsgi', '-b', f'0.0.0.0:{port}'])
#     p.wait()
#
# @hug.cli()
# def infect():
#     script = textwrap.dedent(
#         '\n\n\n'
#         '# function to put daq tools on the path\n'
#         'daq.init() {\n'
#         'export PATH="$HOME/miniconda/bin:$PATH"\n'
#         '    export PATH="$HOME/miniconda3/bin:$PATH"\n'
#         '    export PATH="$HOME/anaconda/bin:$PATH"\n'
#         '    export PATH="$HOME/anaconda3/bin:$PATH"\n'
#         '    export PATH=/Users/rob/anaconda3/bin:$PATH\n'
#         '        . activate daq\n'
#         '}'
#     )
#     bashrc = pathlib.Path(os.path.expanduser('~')).joinpath('.bashrc')
#     with open(bashrc.as_posix(), 'r+') as f:
#         contents = f.read()
#
#         if 'daq.init()' in contents:
#             print('Already infected, nothing to do')
#         else:
#             print(f'\n\ninfecting {bashrc}')
#             f.seek(0, 2)
#             f.write(script)
