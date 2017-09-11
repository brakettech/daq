import os
import sys
import pathlib
import re
# import hug
import django



# def configure_django():
#
#     # find the ambition project path (must start somewhere under project path)
#     path = os.path.realpath(__file__)
#     while path != '/':
#         path = os.path.dirname(path)
#         manage_file = os.path.join(path, 'manage.py')
#         if os.path.isfile(manage_file):
#             # when project path found, configure django
#             proj_path = os.path.dirname(manage_file)
#             sys.path.append(proj_path)
#             os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
#
#             django.setup()
#             return
#     raise Exception('\n\n Couldn\'t configure django properly')
#
#


# @hug.cli()
# def logic():
#     configure_django()
#     pwd = pathlib.Path(__file__)
#     version_file = pwd.parent.parent.joinpath('__init__.py')
#     with open(version_file) as in_file:
#         version_file_contents = in_file.read()
#     version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
#                               version_file_contents, re.M)
#     if version_match:
#         print('braket-daq=={}'.format(version_match.group(1)))
#
#
# def main():
#     logic.interface.cli()
