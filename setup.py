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
    version = "8.0.0"


try:
    requirements = open("requirements.txt").read().split()
except IOError:
    requirements = []


setup(
    name='AwesomeTitleServer',
    url='https://github.com/minhoryang/AwesomeTitle',
    version=version,
    packages=['AwesomeTitleServer'],
    package_dir={'AwesomeTitleServer': 'AwesomeTitleServer'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=True,
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': [
            'minhoryang = AwesomeTitleServer.__main__:main',
        ]
    }
)

