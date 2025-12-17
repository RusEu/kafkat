#!/usr/bin/env python3
"""Setup configuration for Kafkat."""

from setuptools import setup, find_packages
import os

# Read version from package
def get_version():
    """Get version from kafkat/__init__.py"""
    version_file = os.path.join('kafkat', '__init__.py')
    with open(version_file) as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"\'')
    return '2.0.0'

# Read long description from README
def get_long_description():
    """Get long description from README.md"""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return 'A powerful Kafka search CLI tool'

setup(
    name='kafkat',
    version=get_version(),
    description='A powerful Kafka search CLI tool',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Daniel Rus',
    author_email='dani@fsck.ro',
    url='https://github.com/danielrus/kafkat',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click>=8.0.0',
        'kafka-python>=2.0.2',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.10.0',
            'black>=21.0.0',
            'flake8>=3.8.0',
            'mypy>=0.800',
        ]
    },
    scripts=['kafkat/bin/kafkat'],
    entry_points={
        'console_scripts': [
            'kafkat=kafkat.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: System :: Monitoring',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
    keywords='kafka cli search tool message broker',
    project_urls={
        'Bug Reports': 'https://github.com/danielrus/kafkat/issues',
        'Source': 'https://github.com/danielrus/kafkat',
    },
)
