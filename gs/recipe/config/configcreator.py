# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################
from __future__ import absolute_import, unicode_literals
import codecs
from sqlalchemy import (create_engine, MetaData, Table)
from zope.cachedescriptors.property import Lazy
from gs.auth.token.createtoken import (create_token, delete_old_tokens_from_db,
                                        add_token_to_db)
UTF8 = 'utf-8'


class ConfigCreator(object):
    'Create the configuration file for GroupServer'

    # TODO: SMTP off by default?
    configBlock = '''[config-default]
database = default
smtp = on
cache = on
webservice = default'''

    smtpOffBlock = '''[smtp-off]
hostname = localhost
port = 25
queuepath = /tmp/test-mail-queue
processorthread = False'''

    cacheBlock = '''[cache-on]
backend = redis
hostname = localhost
port = 6379

[cache-off]
backend = none
'''

    def __init__(self):
        self.database = {}
        self.smtp = {}
        self.token = None

    def set_database(self, username, password, host, port, name):
        self.database['username'] = username.strip()
        self.database['password'] = password.strip()
        self.database['host'] = host.strip()
        self.database['port'] = port.strip()
        self.database['name'] = name.strip()
        try:
            del self.dsn
        except AttributeError:
            pass

        if not self.database['host']:
            m = '"host" is required'
            raise TypeError(m)
        if not self.database['port']:
            m = '"port" is required'
            raise TypeError(m)
        if not self.database['name']:
            m = '"name" is required'
            raise TypeError(m)

    @Lazy
    def dsn(self):
        if self.database == {}:
            retval = ''
        else:
            d = self.database
            if d['username'] and d['password']:
                d['password'] = ':{0}@'.format(self.database['password'])
            elif d['username'] and not d['password']:
                d['username'] = '{0}@'.format(self.database['username'])
            elif d['password'] and not d['username']:
                d['password'] = ''
            s = 'postgres://{username}{password}{host}:{port}/{name}'
            retval = s.format(**d)
        return retval

    @property
    def databaseBlock(self):
        retval = '[database-default]\ndsn = {0}'.format(self.dsn)
        return retval

    def set_smtp(self, host, port, user, password):
        self.smtp['host'] = host.strip()
        self.smtp['port'] = port.strip()
        self.smtp['user'] = user.strip() if user else ''
        self.smtp['password'] = password.strip() if password else ''

    @property
    def smtpBlock(self):
        r = '''[smtp-on]
queuepath = /tmp/groupserver-default-mail-queue
xverp = True
hostname = {host}
port = {port}'''
        retval = r.format(**self.smtp)
        if self.smtp['user']:
            retval = '{0}\nuser = {1}'.format(retval, self.smtp['user'])
        if self.smtp['password']:
            retval = '{0}\npassword = {1}'.format(retval,
                                                    self.smtp['password'])
        return retval

    def create_token(self):
        self.token = create_token()

    def write_token(self):
        engine = create_engine(self.dsn, echo=False)
        engine.connect()
        metadata = MetaData()
        metadata.bind = engine
        table = Table('option', metadata, autoload=True)
        delete_old_tokens_from_db(table)
        add_token_to_db(table, self.token)

    @property
    def webserviceBlock(self):
        retval = '[webservice-default]\ntoken = {0}'.format(self.token)
        return retval

    def write(self, dest):
        m = self.configBlock + '\n\n' + self.databaseBlock + '\n\n' + \
            self.smtpBlock + '\n\n' + self.smtpOffBlock + '\n\n' + \
            self.cacheBlock + '\n\n' + self.webserviceBlock + '\n\n'
        with codecs.open(dest, 'w', UTF8) as outfile:
            outfile.write(m)
        self.write_token()
