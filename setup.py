import setuptools
from setuptools import setup

setup(
    name="sentimentGpt",
    version="0.0.1",
    install_requires=["transformers"],
    description="Zero-Shot Intent Classification",
    author="frknayk",
    author_email="furkanayik@outlook.com",
    packages=setuptools.find_packages(),
)
