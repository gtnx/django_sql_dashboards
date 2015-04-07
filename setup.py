# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

from distutils.core import setup
from setuptools import find_packages


setup(
    name='django_sql_dashboards',
    version='0.3.2',
    author=u'Guillaume Thomas',
    description='',
    long_description=open('README.txt').read(),
    zip_safe=False,
    install_requires=map(lambda line: line.strip("\n"), open("requirements.txt", "r").readlines()),
    packages=find_packages(),
    include_package_data=True,
)
