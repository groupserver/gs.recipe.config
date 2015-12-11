Changelog
=========

2.1.2 (2015-12-11)
------------------

* Improving the unit-tests by messing with ``stdout`` less

2.1.1 (2014-06-27)
------------------

* Changing the name of the ``username`` parameter in the ``smtp``
  section, because ``gs.email.config.create_emailUtilities`` is
  expecting a ``username``, not a ``user``

2.1.0 (2014-05-26)
------------------

* Making the following parameters optional:
  + ``database_username``
  + ``database_password``
  + ``smtp_user``
  + ``smtp_password``

* Adding UTF-8 support for writing the configuration file.
* Updating the README
* Switching to ``gs.recipe.base`` as the base-class for the
  recipe
* Adding unit-tests

2.0.0 (2012-11-26)
------------------

* Adding Python 2.6 compatibility.
* Upping the version number to bring it in line with the other
  GroupServer products.

1.0.0 (2012-10-19)
------------------

Initial release.

..  LocalWords:  Changelog
