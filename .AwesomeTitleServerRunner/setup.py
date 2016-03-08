#!env python
from subprocess import run, PIPE
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


try:
    version = run(
        "git describe --tags".split(),
        stdout=PIPE
    ).stdout.decode(encoding='UTF-8').strip()
except IOError:
    version = "latest"


setup(
    name='AwesomeTitleServerRunner',
    url='https://github.com/minhoryang/AwesomeTitle',
    version=version,
    packages=['AwesomeTitleServerRunner'],
    package_dir={'AwesomeTitleServerRunner': 'AwesomeTitleServerRunner'},
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
)

