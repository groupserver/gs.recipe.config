# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData, Table
from gs.auth.token.createtoken import create_token, delete_old_tokens_from_db,\
    add_token_to_db


class ConfigCreator(object):

    def __init__(self):
        self.database = {}
        self.smtp = {}
        self.token = None
        self.__dsn = None

    @property
    def configBlock(self):
        retval = '[config-default]\ndatabase = default\nsmtp = on\ncache = on'\
                    '\nwebservice = default'
        return retval

    def set_database(self, username, password, host, port, name):
        self.database['username'] = username.strip()
        self.database['password'] = password.strip()
        self.database['host'] = host.strip()
        self.database['port'] = port.strip()
        self.database['name'] = name.strip()
        self.__dsn = None

    @property
    def dsn(self):
        if self.__dsn is None:
            if self.database == {}:
                self.__dsn = ''
            else:
                d = self.database
                if d['username'] and d['password']:
                    d['password'] = ':%s@' % self.database['password']
                elif d['username'] and not d['password']:
                    d['username'] = '%s@' % self.database['username']
                s = 'postgres://{username}{password}{host}:{port}/{name}'
                self.__dsn = s.format(**d)
        return self.__dsn

    @property
    def databaseBlock(self):
        retval = '[database-default]\ndsn = {0}'.format(self.dsn)
        assert type(retval) == str
        return retval

    def set_smtp(self, host, port, user, password):
        self.smtp['host'] = host.strip()
        self.smtp['port'] = port.strip()
        self.smtp['user'] = user.strip()
        self.smtp['password'] = password.strip()

    @property
    def smtpBlock(self):
        retval = '[smtp-on]\nqueuepath = /tmp/groupserver-default-mail-queue'\
                    '\nxverp = True\nhostname = {host}\n'\
                    'port = {port}'.format(**self.smtp)
        if self.smtp['user']:
            retval = '{0}\nuser = {1}'.format(retval, self.smtp['user'])
        if self.smtp['password']:
            retval = '{0}\npassword = {1}'.format(retval,
                                                    self.smtp['password'])
        assert type(retval) == str
        return retval

    @property
    def smtpOffBlock(self):
        retval = '[smtp-off]\nhostname = localhost\nport = 25\n'\
                'queuepath = /tmp/test-mail-queue\nprocessorthread = False'
        return retval

    @property
    def cacheBlock(self):
        retval = '[cache-on]\nbackend = redis\nhostname = localhost\n'\
                'port = 6379\n\n[cache-off]\nbackend = none\n'
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
        with file(dest, 'w') as outfile:
            outfile.write(self.configBlock + '\n\n')
            outfile.write(self.databaseBlock + '\n\n')
            outfile.write(self.smtpBlock + '\n\n')
            outfile.write(self.smtpOffBlock + '\n\n')
            outfile.write(self.cacheBlock + '\n\n')
            outfile.write(self.webserviceBlock + '\n\n')
        self.write_token()
