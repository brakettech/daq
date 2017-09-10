import pathlib
import re

# def version(path):
#     """Obtain the packge version from a python file e.g. pkg/__init__.py
#     See <https://packaging.python.org/en/latest/single_source_version.html>.
#     """
#     version_file = read(path)
#     version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
#                               version_file, re.M)
#     if version_match:
#         return version_match.group(1)
#     raise RuntimeError("Unable to find version string.")


def main():
    pwd = pathlib.Path(__file__)
    version_file = pwd.parent.parent.joinpath('__init__.py')
    with open(version_file) as in_file:
        version_file_contents = in_file.read()
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file_contents, re.M)
    if version_match:
        print('braket-daq=={}'.format(version_match.group(1)))
