# -*- coding: utf-8 -*-
"""
This module contains the tool of gs.recipe.createtables
"""
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

long_description = (
    file('README.txt').read()
    + '\n' +
    file(os.path.join('docs', 'CONTRIBUTORS.txt')).read()
    + '\n' +
    file(os.path.join('docs', 'CHANGES.txt')).read()
    + '\n'
    )
entry_point = 'gs.recipe.createtables:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

setup(name='gs.recipe.config',
      version=version,
      description="Setup the GroupServer configuration",
      long_description=long_description,
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Zope Public License',
        "Development Status :: 4 - Beta",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux"
        "Programming Language :: Python",
        ],
      keywords='zope groupserver recipe setup instance database config ini',
      author='Michael JasonSmith',
      author_email='mpj17@onlinegroups.net',
      url='',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs', 'gs.recipe'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
        'setuptools',
        'sqlalchemy',
        'zc.buildout',
        'Zope2',
        'gs.auth.token'],
      entry_points=entry_points,
      )
