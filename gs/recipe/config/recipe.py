# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2012, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
import sys
from zc.buildout import UserError
from gs.recipe.base import Recipe
from .configcreator import ConfigCreator


class ConfigRecipe(Recipe):
    "A zc.buildout recipe to create the GroupServer configuration file."

    def install(self):
        """Installer"""
        if self.should_run():
            configCreator = ConfigCreator()
            try:
                configCreator.set_database(
                    self.options.get('database_username', ''),
                    self.options.get('database_password', ''),
                    self.options['database_host'],
                    self.options['database_port'],
                    self.options['database_name'])
                configCreator.set_smtp(self.options['smtp_host'],
                                       self.options['smtp_port'],
                                       self.options.get('smtp_user' ''),
                                       self.options.get('smtp_password', ''))
                configCreator.create_token()
                configCreator.write(self.options['dest'])
            except OSError as e:
                m = '{0} Issue creating the configuration\n{1}\n\n'
                msg = m.format(self.name, e)
                raise UserError(msg)
            except KeyError as e:
                m = '{0} Issue creating the configuration\nThe required '\
                    'paramater "{1}" was not supplied.'
                msg = m.format(self.name, e.args[0])
                raise UserError(msg)
            else:
                self.mark_locked()
                m = 'Configuration written to\n{dest}\n\n'
                sys.stdout.write(m.format(**self.options))
        return tuple()

    def update(self):
        """Updater"""
        self.install()
