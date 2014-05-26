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
import codecs
from mock import MagicMock, patch
import os
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase
from zc.buildout import UserError
import gs.recipe.config.recipe
UTF8 = 'utf-8'


class TestRecipe(TestCase):
    'Test the ConfigRecipe class'
    def setUp(self):
        self.tempdir = mkdtemp()
        self.bindir = os.path.join(self.tempdir, 'bin')
        os.mkdir(self.bindir)
        etcdir = os.path.join(self.tempdir, 'etc')
        os.mkdir(etcdir)
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
        self.destPath = os.path.join(etcdir, 'gsconfig.ini')
        self.options['dest'] = self.destPath

        gs.recipe.config.recipe.ConfigCreator.write_token = \
            MagicMock(return_value='fake-token')

        gs.recipe.config.recipe.sys.stdout = MagicMock()
        gs.recipe.config.recipe.sys.stderr = MagicMock()

    def tearDown(self):
        rmtree(self.tempdir)
        self.tempdir = self.bindir = self.destPath = None

    def assert_should_run_true(self, recipe):
        msg = 'Recipe should run, but ConfigRecipe.should_run returned False.'
        r = recipe.should_run()
        self.assertTrue(r, msg)

    def assert_should_run_false(self, recipe):
        msg = 'Recipe should be locked, but ConfigRecipe.should_run returned '\
                'True.'
        r = recipe.should_run()
        self.assertFalse(r, msg)

    def test_install_standard(self):
        'Test a normal run of the installer'
        recipe = gs.recipe.config.recipe.ConfigRecipe(self.buildout, self.name,
                                                        self.options)
        self.assert_should_run_true(recipe)
        recipe.install()
        self.assert_should_run_false(recipe)

        self.assertTrue(os.path.exists(self.tempdir))
        msg = '{0} is not a regular file.'.format(self.destPath)
        self.assertTrue(os.path.exists(self.destPath), msg=msg)
        with codecs.open(self.destPath, 'r', UTF8) as infile:
            d = infile.read()

        inFile = [k for k in self.options
                    if (('smtp' in k) or ('database' in k))]
        for k in inFile:
            val = self.options[k]
            if val:
                self.assertIn(val, d)

    def test_install_os_error(self):
        'Test a run of the installer that hits an OS error'
        cc = gs.recipe.config.recipe.ConfigCreator
        with patch.object(cc, 'write', autospec=True) as mock_write:
            mock_write.side_effect = OSError

            recipe = gs.recipe.config.recipe.ConfigRecipe(self.buildout,
                                                    self.name, self.options)
            self.assert_should_run_true(recipe)
            self.assertRaises(UserError, recipe.install)
            # Should not be locked after the raise
            self.assert_should_run_true(recipe)

    def test_install_option(self):
        'Ensure that the optional parameters are infact optional'
        options = ['database_username', 'database_password', 'smtp_user',
                    'smtp_password', ]
        for option in options:
            del self.options[option]
            recipe = gs.recipe.config.recipe.ConfigRecipe(self.buildout,
                                                self.name, self.options)
            self.assert_should_run_true(recipe)
            recipe.install()
            self.assert_should_run_false(recipe)
            self.tearDown()
            self.setUp()

    def test_install_option_error(self):
        'Test what happens if a required parameter is omitted'
        requiredOptions = ['database_host', 'database_port', 'database_name',
                            'smtp_host', 'smtp_port']
        for option in requiredOptions:
            o = self.options[option]
            del self.options[option]
            recipe = gs.recipe.config.recipe.ConfigRecipe(self.buildout,
                                                self.name, self.options)
            self.assert_should_run_true(recipe)
            self.assertRaises(UserError, recipe.install)
            # Should not be locked after the raise
            self.assert_should_run_true(recipe)

            self.options[option] = o
