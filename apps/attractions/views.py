import urllib

from copy import copy
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.translation import ugettext as _
from django.http import HttpResponse

from tagging.models import Tag, TaggedItem, ContentType
from tagging.utils import calculate_cloud
from olwidget.widgets import MapDisplay, InfoMap, InfoMapMulti

from attractions.models import Attraction, Hotel, Area, Headline

from forms import TagSearch

map_options = {
    'popups_outside': True,
    'default_lat': -34.0,
    'default_lon': 18.4,
    'default_zoom': 9,
    'zoom_to_data_extent': True,
    'map_div_style': {'width': '620px', 'height': '360px'},
    'layers': ['osm.mapnik', 'google.streets', 'google.satellite', 'google.hybrid',],
    'overlay_style': {'fill_opacity':0.1, 'stroke_color':'#000000'},
}

detail_map_options = {
    'popups_outside': True,
    #'popup_direction': 'br',
    'zoom_to_data_extent': True,
    'cluster': True,
    'map_div_style': {'width': '620px', 'height': '360px'},
    'layers': ['osm.mapnik', 'google.streets', 'google.satellite', 'google.hybrid',],
    #'overlay_style': {'fill_color': '${fillHandler}'},
    #'overlay_style_context': {
    #    'fillHandler': 'function (feature){ return feature.cluster[0].attributes.fill; }',
    #}
}

tag_map_options = detail_map_options.copy()
tag_map_options.update({
    'zoom_to_data_extent': False,
    'default_zoom': 9,
    'default_lat': -34.0,
    'default_lon': 18.7,
})

breadcrumb_base = [
        (_('Home'), '/'),
        (_('All Attractions'), '/attractions/'),
        # why in the hell reverse has error?
]

def area_style(area, lang=None):
    area_style = {'strokeColor': '#000000', 'fill_opacity': 0.7}
    if area.background:
        area_style.update({'fillColor': area.background,})
    else:
        area_style.update({'fillColor': '#e0ffb8',})
    return area_style

attraction_style = {'fill_color': '#0000ff', 'strokeColor': '#0000ff'}
hotel_style = {'fill_color': '#db4ff2', 'strokeColor': '#db4ff2'}

def area_list(request, lang=None):
    """This is the main list with all the featured areas as polygons"""
    from django.utils.translation import get_language
    breadcrumb = [
            (_('Home'), '/'),
            (_('All Regions'), reverse('area_list')),
    ]
    areas = Area.objects.filter(featured=True)
    all_tags = Tag.objects.cloud_for_model(Attraction)
    olmap = InfoMapMulti({'areas':
        [ [ a.poly_simplify(),
            {'html': a.poly_html(), 'style': area_style(a) } ] for a in areas ]},
        options=map_options
    )
    tag_search = TagSearch()
    headlines = Headline.objects.all()

    return render_to_response('attractions/area_list.html', locals(),
            context_instance = RequestContext(request)
    )

def area_detail(request, slug, lang=None):
    area = get_object_or_404(Area, slug=slug)
    areas = Area.objects.filter(featured=True)
    attractions = area.get_attractions()
    tag_search = TagSearch()
    breadcrumb = [
            (_('Home'), '/'),
            (_('All Regions'), reverse('area_list')),
            ( area.nom, '')
    ]
    content = {}
    content.update({'hotels': [
        [ a.point, {'html': a.point_html(),
                    'style': hotel_style,}
        ] for a in area.hotels_list()
    ]})
    content.update({'attractions': [
        [ a.point, {'html': a.point_html(),
                    'style': attraction_style,
        }] for a in attractions
    ]})
    olmap = InfoMapMulti(
        content,
        options=detail_map_options
    )

    return render_to_response('attractions/area_detail.html', locals(),
            context_instance=RequestContext(request))


def attractions_for(request, tag, featured_area=None, lang=None):
    """Get attractions for the given tag, limit to featured_area if given"""

    tag = get_object_or_404(Tag, name=urllib.unquote(tag))
    all_tags = Tag.objects.cloud_for_model(Attraction)
    related_tags = Tag.objects.related_for_model(tag, Attraction,
            counts=True, counts_all=True)
    areas = Area.objects.filter(featured=True)
    tag_search = TagSearch()

    if featured_area:
        # the scope is for a specific featured area
        area = get_object_or_404(Area, slug=featured_area)
        attractions = TaggedItem.objects.get_by_model(Attraction.objects.filter(point__within=area.poly), tag)
        #attractions = Attraction.objects.filter(point__within = area.poly, tags__contains=tag.name)
        poi = {}
        poi.update({'hotels':
            [ [ a.point, {'html': a.point_html(), 'style': hotel_style} ] for a in area.hotels_list() ]
        })
        # put the attractions on top of the hotels
        poi.update({'attractions':
            [[a.point, {'html': a.point_html(), 'style': attraction_style}] for a in attractions]
        })
        template = 'attractions/area_detail.html'
        breadcrumb = [
            (_('Home'), '/'),
            (_('All'), '/attractions/'),
            (_('Tagged %(tag)s' % {'tag': tag.ml} ),
                reverse('attractions_for', kwargs={'tag': tag.name })),
            (_('Within %s' % featured_area),
                reverse('area_detail', kwargs={'slug': featured_area})),
            (_('Within %(area)s and tagged %(tag)s' % {'area': featured_area, 'tag': tag.name}),
                reverse('area_detail', kwargs={'slug': featured_area})),
        ]
    else:
        hotels = []
        for a in areas:
            hotels.extend(a.hotels_list())
        attractions = TaggedItem.objects.get_by_model(Attraction, tag)
        poi = {}
        # add hotels to the list
        poi.update({'hotels': [
            [h.point, {'html': h.point_html(), 'style': hotel_style}] for h in hotels]
        })
        # add the attractions on top
        poi.update({'attractions':
            [[a.point, {'html': a.point_html(), 'style': attraction_style}] for a in attractions]
        })

        template = 'attractions/area_list.html'
        breadcrumb = [
            (_('Home'), '/'),
            (_('All Attractions'), '/attractions/'),
            (_('Attractions For %(tag)s' % {'tag': tag.ml} ),
                reverse('attractions_for', kwargs={'tag': tag.name }))
        ]

    olmap = InfoMapMulti(
        poi,
        options=tag_map_options
    )
    return render_to_response(template, locals(),
            context_instance = RequestContext(request))

def hotel_list(request, lang=None):
    breadcrumb = [
        (_('Home'), '/'),
        (_('All Hotels'), '/attractions/hotels/'),
    ]
    olmap = InfoMap(
        [ [ a.point, a.point_html() ] for a in Hotel.objects.all() ],
        options=map_options
    )
    tags = []
    return render_to_response('attractions/hotel_list.html', locals(),
            context_instance=RequestContext(request))

def hotel_detail(request, slug, lang=None):
    hotel = get_object_or_404(Hotel, slug=slug)
    breadcrumb = [
        (_('Home'), '/'),
        (_('All Hotels'), '/attractions/hotels/'),
        ( hotel.name, request.path),
    ]

    return render_to_response('attractions/hotel_detail.html', locals(),
            context_instance=RequestContext(request))


def vcard(request, model_name, slug, lang=None):
    """
    Returns a vcard representing the item specified in the arguments
    """
    if model_name == 'Attraction':
        item = get_object_or_404(Attraction, slug=slug)
    elif model_name == 'Hotel':
        item = get_object_or_404(Hotel, slug=slug)
    else:
        return Http404
    response = HttpResponse(mimetype='text/x-vcard')
    response['Content-Disposition'] = 'attachment; filename=%s.vcf'%item.slug
    response.write(item.vcard())
    return response

def ajax_tag(request, lang, slug=None):
    """
    Uses the language code passed in to return a list of matching tags
    """
    search_string = request.GET.get('q', None).lower()
    results = ""
    if search_string:
        if slug:
            area = get_object_or_404(Area, slug=slug)
            if lang.lower() == 'en':
                results = ["%s\n"%t.ml for t in area.tags_list() if search_string in t.ml_en.lower()]
            elif lang.lower() == 'it':
                results = ["%s\n"%t.ml for t in area.tags_list() if search_string in t.ml_it.lower()]
        else:
            if lang.lower() == 'en':
                instances = Tag.objects.filter(ml_en__icontains=search_string)
            elif lang.lower() == 'it':
                instances = Tag.objects.filter(ml_en__icontains=search_string)
            for item in instances:
                results += "%s\n"%item.ml.strip()
    return HttpResponse(results, mimetype='text/plain')

def tag_search(request, lang, featured_area=None):
    """
    Proxy for turning a tag search form POST into the appropriate url
    """
    if request.method == 'POST':
        form = TagSearch(request.POST)
        if form.is_valid():
            search_string = form.cleaned_data['tag_search']
            if lang.lower() == 'en':
                instances = Tag.objects.filter(ml_en__iexact=search_string)
            elif lang.lower() == 'it':
                instances = Tag.objects.filter(ml_en__iexact=search_string)
            if instances.count() == 1:
                tag = instances[0].name
                # good to go
                if featured_area:
                    return attractions_for(request, tag=tag, featured_area=featured_area)
                else:
                    return attractions_for(request, tag=tag)

    if featured_area:
        return area_detail(request, slug=featured_area)
    else:
        return area_list(request)

def attr_detail(request, slug, lang=None):
    attraction = get_object_or_404(Attraction, slug=slug)
    areas = Area.objects.filter(featured=True)

    breadcrumb = [
        (_('Home'), '/'),
        (_('All Attractions'), '/attractions/'),
        ( attraction.name, request.path),
    ]

    olmap = InfoMap(
        [ [ attraction.point, attraction.point_html() ] ],
        options=detail_map_options
    )
    if request.GET.get('hotels_within'):
        try:
            km = int(request.GET.get('hotels_within'))
            hotels = attraction.hotels_within(km)
            features = [ [ h.point, h.point_html()] for h in hotels ]
            features.append(
                    [attraction.point,
                        {'html': attraction.point_html(),
                        'style': attraction_style}
                    ]
            )
            olmap = InfoMap(
                    features,
                    options=detail_map_options
            )
        except:
            pass

    return render_to_response('attractions/detail.html', locals(),
            context_instance=RequestContext(request))


#########################
# Other example view that are not used

'''

def areas_for(request, tag):
    breadcrumb = [
            (_('Home'), '/'),
            (_('All Regions'), reverse('area_list')),
            ( tag.ml, '')
    ]
    areas = Area.objects.filter(featured=True)
    areas = [ a for a in areas if tag in a.tags_list()]
    all_tags = Tag.objects.cloud_for_model(Attraction)
    olmap = InfoMap(
        [ [ a.poly_simplify(), a.poly_html() ] for a in areas ],
        options=map_options
    )
    tag_search = TagSearch()

    return render_to_response('attractions/area_list.html', locals(),
            context_instance = RequestContext(request)
    )

def attraction_list(request):
    areas = Area.objects.filter(featured=True)
    tags = Tag.objects.usage_for_model(Attraction, counts=True,
            counts_all=True)

    olmap = InfoMap(
            [
                [ a.point, {'html': a.point_html(), 'style': attraction_style}
            ] for a in Attraction.objects.all()],
        options=map_options
    )

    breadcrumb = [
        (_('Home'), '/'),
        (_('All Attractions'), '/attractions/'),
    ]

    return object_list(request,
            queryset = Attraction.objects.all(),
            extra_context = locals(),
    )


'''
