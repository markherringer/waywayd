How to deploy your changes
==========================

First pull the new code that you want using git.  This should normally be::

  $ git pull origin master

If there are schema changes and we are still in pre-production
you should be able to::

  $ ./manage.py reset attractions
  $ python add_regions.py
  $ python add_hotels.py

If the translations were played with however, you may need to drop the whole db
and start over::

  $ dropdb geo
  $ createdb -T template_postgis -O geo geo
  $ ./manage.py syncdb
  $ python add_regions.py
  $ python add_hotels.py

Then, restart the webserver and the changes should be there::

  $ sudo /etc/init.d/apache2 restart


