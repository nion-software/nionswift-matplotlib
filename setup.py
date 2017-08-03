# -*- coding: utf-8 -*-

"""
To upload to PyPI, PyPI test, or a local server:
python setup.py bdist_wheel upload -r <server_identifier>
"""

import setuptools
import os

setuptools.setup(
    name="nionswift-matplotlib",
    version="0.0.1",
    author="Nion Software",
    author_email="swift@nion.com",
    description="Matplotlib backend for using matplotlib directly within Nion Swift.",
    long_description=open("README.rst").read(),
    url="https://github.com/nion-software/nionswift-matplotlib",
    packages=["nion.matplotlib", ],
    install_requires=['matplotlib'],
    license='Apache 2.0',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.5",
    ],
    include_package_data=True,
    test_suite="nion.matplotlib.test",
    python_requires='~=3.5',
)
