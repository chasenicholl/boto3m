#!/usr/bin/env python3

import boto3m
import sys
from setuptools import setup, find_packages

install_requires = ['boto3']

setup(name='boto3m',
      version=boto3m.__version__,
      description="Boto3 multiprocessing extension.",
      author="Chase Nicholl",
      author_email='me@chasenicholl.com',
      url='https://github.com/chasenicholl/boto3m',
      packages=find_packages(),
      install_requires=install_requires)
