import pathlib
import re
import hug
import subprocess
import os
import textwrap

PWD = pathlib.Path(__file__)
PROJ_PATH = PWD.parent.parent

@hug.cli()
def version():
    version_file = PWD.parent.parent.joinpath('__init__.py')
    with open(version_file) as in_file:
        version_file_contents = in_file.read()
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file_contents, re.M)
    if version_match:
        print('braket-daq=={}'.format(version_match.group(1)))

@hug.cli()
def pwd():
    print(f'\n\nRun this:\ncd {PROJ_PATH.as_posix()}\n')

@hug.cli()
def server(port=None):
    if port is None:
        port = '8000'

    p = subprocess.Popen(['gunicorn', f'--pythonpath={PROJ_PATH}', 'daq.wsgi', '-b', f'0.0.0.0:{port}'])
    p.wait()

@hug.cli()
def infect():
    script = textwrap.dedent(
        '\n\n\n'
        '# function to put daq tools on the path\n'
        'daq.init() {\n'
        'export PATH="$HOME/miniconda/bin:$PATH"\n'
        '    export PATH="$HOME/miniconda3/bin:$PATH"\n'
        '    export PATH="$HOME/anaconda/bin:$PATH"\n'
        '    export PATH="$HOME/anaconda3/bin:$PATH"\n'
        '    export PATH=/Users/rob/anaconda3/bin:$PATH\n'
        '        . activate daq\n'
        '}'
    )
    bashrc = pathlib.Path(os.path.expanduser('~')).joinpath('.bashrc')
    with open(bashrc.as_posix(), 'r+') as f:
        contents = f.read()

        if 'daq.init()' in contents:
            print('Already infected, nothing to do')
        else:
            print(f'\n\ninfecting {bashrc}')
            f.seek(0, 2)
            f.write(script)

@hug.cli()
def update():
    cmd = 'pip install -U braket-daq'
    print(cmd)
    os.system(cmd)
