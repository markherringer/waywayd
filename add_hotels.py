#!/usr/bin/env python
import sys

from os.path import abspath, dirname, join
import os

try:
    import pinax
except ImportError:
    sys.stderr.write("Error: Can't import Pinax. Make sure you are in a virtual environment that has Pinax installed or create one with pinax-boot.py.\n")
    sys.exit(1)

from django.conf import settings
from django.core.management import setup_environ, execute_from_command_line

try:
    import settings as settings_mod # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

# setup the environment before we start accessing things in the settings.
setup_environ(settings_mod)

sys.path.insert(0, join(settings.PINAX_ROOT, "apps"))
sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))



def run():
    from attractions.models import Hotel
    f = file('raw_data/hotels.tsv')
    lines = f.readlines()
    for l in lines[1:-1]:
        li = l.split('\t')
        try:
            h = Hotel()
            h.booking_id = li[0]
            h.name = li[1]
            h.street_address = li[2]
            h.postal_code = li[3]
            h.locality = li[4]
            h.cc1 = li[5]
            h.ufi = li[6]
            h.clas = li[7]
            h.currency_code = li[8]
            h.minrate = li[9]
            h.maxrate = li[10]
            h.preferred = li[11]
            h.number_rooms = int(li[12])
            h.point = 'POINT(%s %s)' % (li[13], li[14])
            h.public_ranking = int(li[15])
            h.url = li[16]
            h.photo_url = li[17]
            h.city_unique = li[28]
            h.city_preferred = li[29]
            h.continent_id = li[30]
            h.set_description(li[18], 'en')
            #19, fr
            #20, es
            #21, de
            #22, nl
            h.set_description(li[23], 'it')
            #24, pt
            #25, ja
            #26, zh
            #27, pl
            h.save()
        except IndexError:
            pass

if __name__ == "__main__":
    run()

