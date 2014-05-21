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
from unittest import TestCase
import gs.recipe.config.configcreator


class TestCreatorDB(TestCase):
    'Test the ConfigCreator class'

    def setUp(self):
        gs.recipe.config.configcreator.create_token = MagicMock()
        gs.recipe.config.configcreator.delete_old_tokens_from_db = MagicMock()
        gs.recipe.config.configcreator.add_token_to_db = MagicMock()

    def test_dsn_no_db(self):
        cc = gs.recipe.config.configcreator.ConfigCreator()
        self.assertEqual('', cc.dsn)

    def test_dsn(self):
        cc = gs.recipe.config.configcreator.ConfigCreator()
        cc.set_database('username', 'password', 'host', 'port', 'name')
        self.assertEqual('postgres://username:password@host:port/name', cc.dsn)

    def test_dsn_no_password(self):
        cc = gs.recipe.config.configcreator.ConfigCreator()
        cc.set_database('username', '', 'host', 'port', 'name')
        self.assertEqual('postgres://username@host:port/name', cc.dsn)

    def test_dsn_no_user(self):
        cc = gs.recipe.config.configcreator.ConfigCreator()
        cc.set_database('', '', 'host', 'port', 'name')
        self.assertEqual('postgres://host:port/name', cc.dsn)

    def test_dsn_password_no_user(self):
        cc = gs.recipe.config.configcreator.ConfigCreator()
        cc.set_database('', 'password', 'host', 'port', 'name')
        self.assertEqual('postgres://host:port/name', cc.dsn)

    def test_dsn_no_host(self):
        cc = gs.recipe.config.configcreator.ConfigCreator()
        self.assertRaises(TypeError, cc.set_database,
                            ('', '', '', 'port', 'name'))

    def test_dsn_no_port(self):
        cc = gs.recipe.config.configcreator.ConfigCreator()
        self.assertRaises(TypeError, cc.set_database,
                            ('', '', 'host', '', 'name'))

    def test_dsn_no_name(self):
        cc = gs.recipe.config.configcreator.ConfigCreator()
        self.assertRaises(TypeError, cc.set_database,
                            ('', '', 'host', 'port', ''))

    def test_db_block(self):
        cc = gs.recipe.config.configcreator.ConfigCreator()
        cc.set_database('', '', 'host', 'port', 'name')
        self.assertIn('dsn = postgres://host:port/name', cc.databaseBlock)


class TestCreatorSMTP(TestCase):
    'Test the SMTP block'

    def setUp(self):
        gs.recipe.config.configcreator.create_token = MagicMock()
        gs.recipe.config.configcreator.delete_old_tokens_from_db = MagicMock()
        gs.recipe.config.configcreator.add_token_to_db = MagicMock()

    def test_smtp_host(self):
        cc = gs.recipe.config.configcreator.ConfigCreator()
        cc.set_smtp('host', 'port', 'user', 'password')
        self.assertIn('hostname = host', cc.smtpBlock)

    def test_smtp_port(self):
        cc = gs.recipe.config.configcreator.ConfigCreator()
        cc.set_smtp('host', 'port', 'user', 'password')
        self.assertIn('port = port', cc.smtpBlock)


class TestCreatorWebservice(TestCase):
    'Test the Webserfice block'

    def setUp(self):
        gs.recipe.config.configcreator.create_token = MagicMock()
        gs.recipe.config.configcreator.delete_old_tokens_from_db = MagicMock()
        gs.recipe.config.configcreator.add_token_to_db = MagicMock()

    def test_smtp_host(self):
        cc = gs.recipe.config.configcreator.ConfigCreator()
        cc.token = 'foo'
        self.assertIn('token = ', cc.webserviceBlock)
