# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django_sql_dashboards',
    version='0.0.3-2',
    author=u'Guillaume Thomas',
    description='',
    long_description=open('README.txt').read(),
    zip_safe=False,
    install_requires=[
       "Django==1.5",
       "django-bootstrap3>=2.3.0",
       "MySQL-python",
       "South"
    ],
    packages = find_packages(),
    include_package_data=True,
)
