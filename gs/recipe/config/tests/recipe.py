# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals
from mock import MagicMock
import os
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase
# from zc.buildout import UserError
import gs.recipe.config.recipe
UTF8 = 'utf-8'


class TestRecipe(TestCase):
    'Test the ConfigRecipe class'
    def setUp(self):
        self.tempdir = mkdtemp()
        self.bindir = os.path.join(self.tempdir, 'bin')
        os.mkdir(self.bindir)
        vardir = os.path.join(self.tempdir, 'var')
        os.mkdir(vardir)

        self.buildout = {'buildout': {'directory': self.tempdir,
                                        'bin-directory': self.bindir, }, }
        self.name = 'postfix'
        self.options = {}
        self.options['recipe'] = 'gs.recipe.config'
        self.options['database_username'] = 'example_db_user'
        self.options['database_password'] = 'example_db_password'
        self.options['database_host'] = 'db.example.com'
        self.options['database_port'] = '5433'
        self.options['database_name'] = 'example_db'
        self.options['smtp_host'] = 'smtp.example.com'
        self.options['smtp_port'] = '2525'
        self.options['smtp_user'] = ''
        self.options['smtp_password'] = ''

        self.recipe = gs.recipe.config.recipe.ConfigRecipe(self.buildout,
                                                    self.name, self.options)

        gs.recipe.config.recipe.sys.stdout = MagicMock()
        gs.recipe.config.recipe.sys.stderr = MagicMock()

    def tearDown(self):
        rmtree(self.tempdir)
