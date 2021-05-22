from setuptools import find_packages
from setuptools import setup

setup(
    name='typify',
    version='1.0.0',
    description='This package contains the typify application for the bachelor \
    thesis project "Typify a researcher or research group".',
    author='Jaap Stefels',
    author_email='jaapstefels@gmail.com',
    url='https://github.com/jaapstefels/typify',
    packages=find_packages(),
    install_requires=[
        'scholarly',
        'cso-classifier',
        'dash',
        'nltk',
        'plotly==4.14.3'
    ]
)