# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in expense_request/__init__.py
from expense_request import __version__ as version

setup(
	name='expense_request',
	version=version,
	description='ERPNext Expenses',
	author='Bantoo',
	author_email='hello@thebantoo.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
