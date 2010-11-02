from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import Template, Context
from django.template.defaultfilters import slugify
from django.contrib.gis.db import models
from django.contrib.gis.measure import D
from django.utils.translation import ugettext_lazy as _, ugettext as __
from tagging.models import Tag, TaggedItem
from tagging.fields import TagField
from multilingual.translation import Translation
from multilingual.manager import Manager as TranslationManager

from attractions.constants import COUNTRY_LIST

tag_cloud_template = Template("""
<ul id="cloud">
{% if tags %}
{% for t in tags %}
<li class="tag-{{t.font_size}}">
<a href="{% url attractions_for tag=t.url_name %}area/{{area.slug}}"> {{ t.ml}} ({{ t.count }})</a>
</li>
{% endfor %}
{% else %}
<li><b>"""+__("Not Tagged")+"""</b></li>
{% endif %}
</ul>
""")

tag_cloud_small_template = Template("""
{% if tags %}
{% for t in tags %}
<span class="tag-{{t.font_size}}">
<a href="{% url attractions_for tag=t.url_name %}{% if area %}area/{{area.slug}}{% endif %}"> {{ t.ml}} ({{ t.count }})</a>
</span>
{% endfor %}
{% else %}
<strong>"""+__("Not Tagged")+"""</strong>
{% endif %}""")

point_html_template = Template("""
<div class="point-popup">
{{point.hcard}}
<p><a href="/attractions/attraction/{{point.slug}}/vcard">"""+__('Import details to your contacts')+"""</a></p>
{{point.render_tag_list}}
</div>
""")

hotel_point_template = Template("""
{% load i18n %}
{% get_current_language as LANGUAGE_CODE %}
<div class="point-popup">
{{point.hcard}}
<div>
<p><a href="/attractions/hotel/{{point.slug}}/vcard">"""+__('Import details to your contacts')+"""</a> |
<a href="{{point.url}}?aid=325529&lang={{LANGUAGE_CODE}}" target="new">{% trans "Book it on booking.com" %}</a></p>
<a href="{{point.url}}?aid=325529&lang={{LANGUAGE_CODE}}" target="new"><img src="{{ STATIC_URL }}images/booking_logo.gif" alt="booking.com logo"/></a>
</div>
<div style="float:right;">
{% trans "Price Range" %}:<br>
{{point.minrate}} - {{point.maxrate}} {{point.currency_code}}
</div>
{% if point.thumb %}
<img src="{{point.thumb.url}}" alt="{% trans 'no image available' %}" />
{% endif %}
{{point.render_cloud}}
</div>
""")

area_poly_template = Template("""
<div class="point-popup">
<h4><a href="{{area.get_absolute_url}}">{{area.nom}}</a></h4>
<p>{{area.headline|safe}}</p>
{{area.render_tag_list}}
</div>
""")

area_description_template = Template("""
<!-- accordion -->
{% for description in descriptions%}
{{description.description_html}}
{% endfor %}""")

description_template = Template("""
<h2 class="trigger">
    <a href="#">{{description.title}}</a>
</h2>
<div class="toggle_container" style="display: none">
    <div class="block">
    {{description.content|safe}}
    </div>
</div>
<div class="break"></div>
""")

hcard_template = Template( """{% load i18n %}
{% get_current_language as LANGUAGE_CODE %}
<div class="vcard">
    <div class="fn n">
        {% if item.url %}<a href="{{item.url}}{% if aid %}?aid=325529&lang={{LANGUAGE_CODE}}{% endif %}" class="url" target="new">{% endif %}
            <span class="org">{{item.name}}</span>
        {% if item.url %}</a>{% endif %}
    </div>
        <span class="adr">
            {% if item.street_address %}<div class="street-address">{{item.street_address}}</div>{% endif %}
            {% if item.locality %}<span class="locality">{{item.locality}}</span>&nbsp;{% endif %}
            {% if item.region %}<span class="region">{{item.region}}</span>&nbsp;{% endif %}
            {% if item.postal_code %}<span class="postal-code">{{item.postal_code}}</span>&nbsp;{% endif %}
            {% if item.country %}<span class="country-name">{% if item.get_country_display %}{{item.get_country_display}}{% else %}{{item.country}}{% endif %}</span>{% endif %}
        </span>
        <br/>
        {% if item.email %}<b>Email</b>: <a class="email" href="mailto:{{item.email}}">{{item.email}}</a><br/>{% endif %}
        {% if item.tel_work %}<b>Telephone</b>: <span class="tel"><span class="value">{{item.tel_work}}</span> [<abbr class="type" title="work">"""+__('work')+"""</abbr>]</span><br/>{% endif %}
        {% if item.tel_home %}<b>Telephone</b>:<span class="tel"><span class="value">{{item.tel_home}}</span> [<abbr class="type" title="home">"""+__('home')+"""</abbr>]</span>{% endif %}
</div>
""")

vcard_template = Template("""BEGIN:VCARD
VERSION:3.0
N:{{item.slug}};;;;
FN:{{item.name}}
ORG:{{item.name}};
{% if item.email %}EMAIL;type=INTERNET;type=WORK;type=pref:{{ item.email }}{% endif %}
{% if item.tel_work %}TEL;type=WORK;type=pref:{{ item.tel_work }}{% endif %}
{% if item.tel_home %}TEL;type=HOME:{{ item.tel_home }}{% endif %}
item1.ADR;type=WORK;type=pref:{{item.street_address}};;{{item.locality}};{{item.region}};{{item.postal_code}};{% if item.get_country_display %}{{item.get_country_display}}{% else %}{{item.country}}{% endif %}
{% if item.url %}item2.URL;type=pref:{{ item.url }}{% endif %}
END:VCARD """)

def render_node(template, dictionary):
    return template.render(Context(dictionary))

class GeoTranslationManager(models.GeoManager, TranslationManager):
    pass

class Hotel(models.Model):
    booking_id = models.CharField(max_length=15, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    url = models.URLField(max_length=255, verify_exists=True, blank=True)
    email = models.EmailField(blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    locality = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    # postal_code is the name specified by the vCard format that forms the basis
    # of the hCard microformat. Synonymous with zip code... ;-)
    postal_code = models.CharField(max_length=20, blank=True) 
    # by defining countries like this we can piggy back on Django's translation
    # framework
    country = models.CharField(max_length=3, blank=True, choices=COUNTRY_LIST) 
    tel_work = models.CharField(max_length=20, blank=True)
    tel_home = models.CharField(max_length=20, blank=True)
    cc1 = models.CharField(max_length=5, blank=True)
    ufi = models.CharField(max_length=20, blank=True)
    clas = models.CharField(max_length=5, blank=True)
    currency_code = models.CharField(max_length=10, blank=True)
    minrate = models.CharField(max_length=15, blank=True)
    maxrate = models.CharField(max_length=15, blank=True)
    preferred = models.CharField(max_length=20, blank=True)
    number_rooms = models.IntegerField(blank=True, null=True)

    point = models.PointField()

    public_ranking = models.IntegerField(blank=True, null=True)
    photo_url = models.CharField(max_length=255, blank=True)
    thumb = models.ImageField(upload_to="thumbs", blank=True)

    objects = GeoTranslationManager()

    class Translation(Translation):
        description = models.TextField(blank=True)

    city_unique = models.CharField(max_length=255, blank=True)
    city_preferred = models.CharField(max_length=255, blank=True)
    continent_id = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('attractions.views.hotel_detail',(), {'slug':self.slug,})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Hotel, self).save(*args, **kwargs)
        if self.photo_url and not self.thumb:
            import urllib
            import Image
            import os
            from django.core.files import File
            f = urllib.urlretrieve(self.photo_url)
            size = 128, 128
            im = Image.open(f[0])
            im.thumbnail(size)
            dir_name = os.path.dirname(f[0])
            img_name = str(self.id) + os.path.basename(self.photo_url)
            im.save(os.path.join(dir_name, "thumb" + img_name))
            self.thumb.save(os.path.basename("thumb" + self.photo_url),
                File(open(os.path.join(dir_name, "thumb" + img_name)))
            )

    def point_html(self):
        context = {'point': self, 'STATIC_URL': settings.STATIC_URL}
        return render_node(hotel_point_template, context)

    def hcard(self):
        """
        Returns the information about this hotel as an appropriately marked-up
        hCard microformat
        """
        context = {'item': self, 'aid': True}
        return render_node(hcard_template, context)

    def vcard(self):
        """
        Returns information about this hotel as an appropriately marked-up
        vcard
        """
        context = {'item': self}
        return render_node(vcard_template, context)

class Area(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    poly = models.PolygonField()
    objects = models.GeoManager()
    featured = models.BooleanField()
    background = models.CharField(max_length=32, help_text="e.g. #FFAE00",
                                  null=True, blank=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    flickr_group = models.CharField(max_length=32,
                                    help_text="e.g. 1340769@N24",
                                    null=True, 
                                    blank=True)

    tags = TagField(
            help_text=
            "We can also get tags through the features but it is more expensive"
    )

    class Translations(Translation):
        nom = models.CharField(max_length=255)
        headline = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('attractions.views.area_detail', (), {'slug':self.slug})

    def get_attractions(self):
        return Attraction.objects.filter(point__within = self.poly)

    def attraction_tags(self):
        return Tag.objects.cloud_for_model(Attraction,
                filters = {'point__within':self.poly },
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Area, self).save(*args, **kwargs)

    def poly_html(self):
        context = {'area': self}
        return render_node(area_poly_template, context)

    def render_tag_list(self):
        '''Produce the html for the popup'''
        context = { 'tags':
                Tag.objects.cloud_for_model(Attraction, filters={'point__within': self.poly}, counts_all=False)[:10],
                'area': self,
        }
        return render_node(tag_cloud_small_template, context)

    def render_cloud(self):
        '''Produce the html for the cloud'''
        context = { 'tags':
                Tag.objects.cloud_for_model(Attraction,
                filters={'point__within': self.poly}, counts_all=False),
                   'area': self,
        }
        return render_node(tag_cloud_template, context)

    def tags_list(self):
        '''Return just the list of tag names'''
        return Tag.objects.usage_for_queryset(
                Attraction.objects.filter(point__within=self.poly)
        )
    def poly_simplify(self):
        return self.poly.simplify(tolerance=0.001, preserve_topology=True)

    def hotels_list(self):
        '''Return the list of hotels in this area'''
        return Hotel.objects.filter(point__within=self.poly)

    def render_description(self):
        """ Produce the HTML for the description accordion widget"""
        context = {"descriptions": self.descriptions.order_by('order')}
        return render_node(area_description_template, context)

class AreaDescription(models.Model):
    """
    To hold a description item (to be displayed in the accordion widget)
    relating to a specific area. 
    """
    area = models.ForeignKey(Area, related_name="descriptions")
    order = models.IntegerField(help_text="Indicates ordering item", default=1)

    class Translations(Translation):
        title = models.CharField(max_length=64)
        content = models.TextField()

    def description_html(self):
        """ Produces HTML for an individual description item """
        context = {'description': self}
        return render_node(description_template, context)

    class Meta:
        ordering = ['area', 'order']

class Attraction(models.Model):
    '''h/vcard data for a place'''
    # The name is a noun so probably *shouldn't* need translating
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    # GEO
    point = models.PointField()
    objects = GeoTranslationManager()
    #objects = models.GeoManager()


    url = models.URLField(max_length=255, verify_exists=True, blank=True)
    email = models.EmailField(blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    locality = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    # postal_code is the name specified by the vCard format that forms the basis
    # of the hCard microformat. Synonymous with zip code... ;-)
    postal_code = models.CharField(max_length=20, blank=True) 
    # by defining countries like this we can piggy back on Django's translation
    # framework
    country = models.CharField(max_length=3, blank=True, choices=COUNTRY_LIST) 
    tel_work = models.CharField(max_length=20, blank=True)
    tel_home = models.CharField(max_length=20, blank=True)

    tags=TagField()
    featured = models.BooleanField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Translation fields
    class Translation(Translation):
        description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('attractions.views.attr_detail',(), {'slug':self.slug,})

    # TAGS
    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def add_tag(self, tag):
        Tag.objects.add_tag(self, tag)

    def related_tags(self):
        '''Tags of items that have all of the Tags'''
        return Tag.objects.related_for_model(self.tags, self.__class__, counts=True)

    def get_cloud(self):
        '''The raw list of tags with count and font_size attributes'''
        return Tag.objects.cloud_for_model(Attraction,
                filters={'slug':self.slug}, counts_all=False)

    def render_tag_list(self):
        '''Produce the html for the popup'''
        context = { 'tags':
                Tag.objects.cloud_for_model(Attraction, filters={'slug': self.slug}, counts_all=False)[:10]
        }
        return render_node(tag_cloud_small_template, context)

    def render_cloud(self):
        '''Produce the html for the cloud'''
        context = { 'tags': self.get_cloud(), }
        return render_node(tag_cloud_template, context)

    def related_attractions(self, num=None):
        '''Instances of this model that have a tag in common'''
        return TaggedItem.objects.get_related(self, self.__class__, num=num)

    def attractions_common_tag(self):
        '''Same as related_attractions but with a different method'''
        return TaggedItem.objects.get_union_by_model(
                self.__class__.objects.exclude(slug=self.slug),
                self.tags
        )
    # See get_by_model, get_intersection_by_model on the TaggedItem.objects.

    # GEO methods
    def get_areas(self):
        return Area.objects.filter(poly__contains=self.point)

    def point_html(self):
        context = {'point': self, 'model_class': self.__class__.__name__.lower()}
        return render_node(point_html_template, context)

    def hotels_within(self, km):
        return Hotel.objects.filter(point__distance_lte=(self.point, D(km=km)))

    def hcard(self):
        """
        Returns the contact information about this attraction as an appropriately marked-up
        hCard microformat
        """
        context = {'item': self}
        return render_node(hcard_template, context)

    def vcard(self):
        """
        Returns information about this attraction as an appropriately marked-up
        vcard
        """
        context = {'item': self}
        return render_node(vcard_template, context)

class Headline(models.Model):
    """
    To hold a Headline item (to be displayed in the accordion widget)
    on the home page
    """
    order = models.IntegerField(help_text="Indicates ordering item", default=1)

    class Translations(Translation):
        title = models.CharField(max_length=64)
        content = models.TextField()

    def html(self):
        """ Produces HTML for an individual description item """
        context = {'description': self}
        return render_node(description_template, context)

    class Meta:
        ordering = ['order']

class Feedback(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=255)
    message = models.TextField()

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name + self.email + str(self.added)


