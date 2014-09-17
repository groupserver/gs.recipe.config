====================
``gs.recipe.config``
====================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A ``zc.buildout`` recipe to create the GroupServer configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-05-26
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

Introduction
============

The core GroupServer_ configuration is provided by an ``INI``
file in the ``etc/`` directory of the GroupServer
installation. This product supplies a ``zc.buildout`` recipe_
[#buildout]_ that creates this configuration file. It is
controlled by a number of parameters_ that are set in the
buildout-configuration, and a `lock file`_.

The ``gs.config`` product reads in the data from the ``INI`` file
[#config]_.

Recipe
======

Calling the recipe is done by ``buildout``. It is configured like
other ``zc.buildout`` recipes::

  [create-config]
  recipe = gs.recipe.config
  dest = ${buildout:etc-directory}/gsconfig.ini
  database_host = ${config:pgsql_host}
  database_port = ${config:pgsql_port}
  database_username = ${config:pgsql_user}
  database_password = ${config:pgsql_password}
  database_name = ${config:pgsql_dbname}
  smtp_host = ${config:smtp_host}
  smtp_port = ${config:smtp_port}
  smtp_user = ${config:smtp_user}
  smtp_password = ${config:smtp_password}

The values for the parameters_ are set in the main ``config.cfg``
file, except for the ``dest``, which is defined by ``buildout``
itself.

When called the recipe will create the ``gsconfig.ini`` file, and
define both *outgoing* SMTP and database connectivity.

Parameters
----------

The following parameters must be supplied to the recipe.

``dest``:
  The destination configuration file. 

``database_host``:
  The host-name of the PostgreSQL database.

``database_port``:
  The port that the PostgreSQL database is listening on.

``database_name``:
  The name of the PostgreSQL database that will store all the
  tables used by GroupServer.

``smtp_host``:
  The name of the *outgoing* SMTP host.

``smtp_port``:
  The port that the *outgoing* SMTP host listens to.

The following four parameters are **optional.**

``database_username``:
  The name of the PostgreSQL database user.

``database_password``:
  The password that the PostgreSQL database user will use to log
  in. (Yes, this will be written down in the ``INI`` file.)

``smtp_user``:
  The name used to log into the *outgoing* SMTP host.

``smtp_password``:
  The password used to log into the *outgoing* SMTP host. (Yes,
  this will be written down in the ``INI`` file.)

Lock file
=========

To ensure the ``INI`` file is only crated once a *lock file* is
crated, ``var/create-config.cfg``, within the GroupServer
installation directory. (The name is actually taken from the name
of the section in the configuration file.)

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.recipe.config/
- Questions and comments to http://groupserver.org/groups/develop/
- Report bugs at https://redmine.iopen.net/projects/groupserver/

.. [#buildout] See `Buildout.org <http://www.buildout.org/en/latest/>`_
               for more information.
.. [#config] See https://source.iopen.net/groupserver/gs.config/
.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

..  LocalWords:  config groupserver mpj buildout zc smtp dest
..  LocalWords:  dbname ini cfg gsconfig username http
