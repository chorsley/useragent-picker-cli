"""
Generates random but realistic user agents on a command line (or via API)
"""
from setuptools import find_packages, setup

from os import path
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="useragent-picker-cli",
    version="0.1.4",
    url="https://github.com/chorsley/useragent-picker-cli",
    license="BSD",
    author="Chris Horsley",
    author_email="cmrhorsley@gmail.com",
    description="Generates random but realistic user agents on a command line (or via API)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=[
        "aiocontextvars==0.2.2; python_version < '3.7'",
        "certifi==2020.6.20",
        "chardet==3.0.4",
        "contextvars==2.4; python_version < '3.7'",
        "docopt==0.6.2",
        "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "immutables==0.14; python_version >= '3.5'",
        "loguru==0.5.1",
        "requests==2.25.1",
        "ua-parser==0.10.0",
        "urllib3==1.25.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
        "user-agents==2.1",
    ],
    dependency_links=[],
    entry_points={"console_scripts": ["uagen = ua_gen.cli:main",],},
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        "Development Status :: 4 - Beta",
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
