from setuptools import setup, find_namespace_packages

setup(
    name='benchtools',
    version='0.1',
    packages=find_namespace_packages(),
    install_requires=[
        'Click', 'ollama', 'pandas', 'yaml'
    ],
    entry_points={
        'console_scripts': [
            'benchtool = benchtools.cli:benchtool',
        ],
    },
)