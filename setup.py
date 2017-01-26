import os

from setuptools import setup

setup(
    name = "media_inventory",
    version = "0.0.1",
    author = "Lucian Petrut",
    author_email = "petrutlucian94@gmail.com",
    description = ("A small app exposing a XML REST API"),
    packages=['media_inventory'],
    install_requires=['flask']
)
