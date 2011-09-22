#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

VERSION='0.1-beta'

setup(
    name = 'django-chameleon',
    version = VERSION,
    url = 'https://github.com/slok/django-chameleon',
    license = 'BSD',
    description = u'Django dynamic theme (template) changer',
    author = 'Xabier (slok) Larrakoetxea',
    author_email = 'slok69@gmail.com',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = [
        'chameleon',
    ],
    install_requires = ['setuptools'],
)
