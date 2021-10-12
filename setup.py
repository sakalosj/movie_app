# Always prefer setuptools over distutils
from os.path import splitext, basename

from setuptools import setup, find_namespace_packages, find_packages
from setuptools.glob import glob

setup(
    name="movie_app",
    version="0.1.0",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    author="Jan Sakalos",
    author_email="sakalosj@gmail.com",
    package_dir={'': 'src'},
    packages=find_packages('./src'),
    py_modules=['app_config', 'log'],
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'movie_app_cli=cli.movie_app_cli:movie_app_cli',
        ]
    }
)
