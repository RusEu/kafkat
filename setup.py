#!/usr/bin/env python

from distutils.core import setup

import setuptools  # noqa

setup(
    name='kafkat',
    version='1.0',
    description='Kafka Python Cli',
    author='Daniel Rus',
    author_email='dani@fsck.ro',
    url="",
    packages=[
        'kafkat',
        'kafkat/common'
    ],
    install_requires=[
        'click==7.1.2',
        'kafka-python==2.0.2'
    ],
    scripts=["./kafkat/bin/kafkat"]
)
