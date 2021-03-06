= Prepare your system =

You need to be running Django  >= 1.2.1 for the site to work. Ubuntu Lucid
and Debian Lenny ship with older versions so do a manual build. We
walk through this
setup using the python virtual environment system.

== Create working dir ==

```
cd /home
sudo mkdir -p web/citta-tim
cd web/waywayd
```

== Source Checkout ==

```
git clone git@github.com:markherringer/cittadelcapo.git
```

== Setup python virtual environment ==



We install Python in a virtual environment on Ubuntu and Debian, to be
able to install Django 1.2 separate from the "System Python" and avoid
conflicts.

If you do not have the Python virtualenv software, get it with:

```
sudo apt-get install python-virtualenv
```

Now, start the Python virtual environment setup. We install Python in
the "python" subfolder of the project directory and then activate the
virtual environment.

```
virtualenv --no-site-packages python
source python/bin/activate
```


== Install some development dependencies ==

```
sudo apt-get install libpq-dev libpq4 libpqxx-dev
```

Install easy_install so that we can use pip thereafter:

```
easy_install pip
```


== Install django and required django apps ==

To install django, django authentication etc into our virtual environment do:

```
pip install pinax
pip install django
pip install psycopg2
pip install pil
pip install django-avatar
pip install django-friends
pip install django-profiles
pip install django-rosetta
pip install django-olwidget
pip install django-multilingual-ng
pip install django-cms
pip install django-socialauth
pip install django-debug-toolbar
pip install django-extensions
pip install django-microblogging
pip install -r cittadelcapo/REQUIREMENTS.txt
```



= Database setup =

If you havent already done so, we suggest installing PostGIS into your
template1 so that
it is available to any database you create:

```
createlang plpgsql template1
psql template1 < /usr/share/postgresql-8.3-postgis/lwpostgis.sql
psql template1 < /usr/share/postgresql-8.3-postgis/spatial_ref_sys.sql
```

Create the database using:

```
createdb waywayd
```

== For an empty database: ==

Clone the local settings file and modify it as needed:

```
cp local_settings.pyEXAMPLE local_settings.py
vim local_settings.py
```


Sync the model to the db (dont do this is you plan to restore an
existing db as explained in the next section):

```
python manage.py syncdb
```


The django fixtures included with this project should populate the
initial database when you run the above command.

= Setup apache (mod_wsgi way) =

The assumption is that you are using name based virtual hosts and that the
catalogue will run at the root of such a virtual host. Add to you
apache site config:

Modify as appropriate a copy of the apache-site-wsgi.templ file found
in the apache
dir in the source tree then link it to apache.


```
cd apache
cp apache-site-wsgi.templ waywayd-wsgi
```

(full text of apache-site-wsgi.templ at the end of this document)


Now create a symlink:

```
sudo ln -s waywayd-wsgi /etc/apache2/sites-available/waywayd-wsgi
```

Also do:

```
sudo apt-get install libapache2-mod-wsgi
```

Now deploy the site:

```
sudo a2ensite waywayd-wsgi
sudo /etc/init.d/apache reload
```



= Check settings.py! =

Go through settings.py (after first copying it from settings.py.templ
if needed) and check all the details are consistent in that file.

For me, the basic_profile app had to be renamed:

```
basic_profiles
```

to

```
profiles
```

I also had to comment out:

```
#"account.context_processors.openid",
```

See: http://groups.google.com/group/pinax-users/browse_thread/thread/e0454a1d5c768a70/04e7988fa87d76df

= ER Diagram =

You can generate an ER diagram for the application using the django
command extensions:


To generate the graph use:

```
python manage.py graph_models cittadelcapo > docs/er_diagram.dot
cat docs/er_diagram.dot | dot -Tpng -o docs/er_diagram.png ; display
docs/er_diagram.png
```

= SVN Ignoring files =

Please read this:

http://stackoverflow.com/questions/116074/how-to-ignore-a-directory-with-svn

so that files that do not belong in svn are not shown in the status list.

= Troubleshooting =

== settings.py not found ==

This is usually a symptom that one of the imports withing settings.py
failed. Test by doing:

```
python
```

Then at the python prompt do

```
import settings
```

The error you obtain there (if any) will be more descriptive.




= Apache config =

```
<VirtualHost *>
 ServerName waywayd.localhost
 ServerAdmin webmaster@localhost
 DocumentRoot /var/www
 <Directory />
   Options FollowSymLinks
   AllowOverride None
 </Directory>
 <Directory /var/www/>
   Options Indexes FollowSymLinks MultiViews
   AllowOverride None
   Order allow,deny
   allow from all
 </Directory>

 ErrorLog /var/log/apache2/waywayd.error.log

 # Possible values include: debug, info, notice, warn, error, crit,
 # alert, emerg.
 LogLevel warn

 CustomLog /var/log/apache2/waywayd.access.log combined

 Alias /waywayd /home/web/waywayd/cittadelcapo

 #
 # Added by Tim for django
 #
 WSGIScriptAlias / /home/web/waywayd/cittadelcapo/deploy/pinax.wsgi

 <Directory "/home/web/waywayd/cittadelcapo/apache">
   Order deny,allow
   Allow from all
 </Directory>

 WSGIDaemonProcess waywayd user=timlinux group=timlinux processes=2
threads=10 python-path=/home/web/waywayd/python/lib/python2.6/site-packages
 WSGIProcessGroup waywayd

 #added by Gavin
 Alias /media/ "/home/web/waywayd/cittadelcapo/media/"
 <Directory /home/web/waywayd/cittadelcapo/media>
   Order deny,allow
   Allow from all
 </Directory>

 Alias /site_media/static/admin/
"/home/web/waywayd/python/lib/python2.6/site-packages/django/contrib/admin/media/"
 <Directory /home/web/waywayd/python/lib/python2.6/site-packages/django/contrib/admin/media/>
   Order deny,allow
   Allow from all
 </Directory>

 Alias /site_media/static/olwidget/
"/home/web/waywayd/python/lib/python2.6/site-packages/olwidget/media/"
 <Directory /home/web/waywayd/python/lib/python2.6/site-packages/olwidget/media/>
   Order deny,allow
   Allow from all
 </Directory>
</VirtualHost>
```

