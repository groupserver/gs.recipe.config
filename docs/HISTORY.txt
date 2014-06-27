Changelog
=========

2.1.1 (2014-06-27)
------------------

* Changed the name of the ``username`` parameter in the ``smtp``
  section, because ``gs.email.config.create_emailUtilities`` is
  expecting a ``username``, not a ``user``.

2.1.0 (2014-05-26)
------------------

* Made the following parameters optional:
  + ``database_username``
  + ``database_password``
  + ``smtp_user``
  + ``smtp_password``

* Added UTF-8 support for writing the configuration file.
* Updated the README.
* Switched to ``gs.recipe.base`` as the base-class for the
  recipe.
* Added unit-tests.

2.0.0 (2012-11-26)
------------------

* Added Python 2.6 compatibility.
* Upped the version number to bring it in line with the other
  GroupServer products.

1.0.0 (2012-10-19)
------------------

* Initial release.
