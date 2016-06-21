#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup


DIR = os.path.dirname(os.path.abspath(__file__))

version = '0.1.0'

readme = open(os.path.join(DIR, 'README.md')).read()


setup(
    name='ethereum-contract',
    version=version,
    description="""Ethereum Contract""",
    long_description=readme,
    author='Piper Merriam',
    author_email='pipermerriam@gmail.com',
    url='https://github.com/pipermerriam/ethereum-contract',
    include_package_data=True,
    install_requires=[
        "pysha3>=0.3",
        "rlp>=0.4.6",
        "ethereum-abi-utils>=0.2.1",
    ],
    py_modules=['eth_contract'],
    license="MIT",
    zip_safe=False,
    keywords='ethereum',
    packages=[
        "eth_contract",
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
