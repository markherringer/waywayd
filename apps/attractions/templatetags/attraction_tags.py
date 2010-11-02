from django import template
from tagging.utils import LOGARITHMIC
from tagging.utils import calculate_cloud

register = template.Library()

@register.inclusion_tag('attractions/breadcrumb.html')
def show_breadcrumb(nodes):
    return { 'nodes': nodes }


@register.inclusion_tag('attractions/cloud_for_tags.html')
def cloud(tags, steps=4, distribution=LOGARITHMIC):
    '''Takes a queryset of Tags with counts and renders the clound html'''
    tags = calculate_cloud(list(tags), steps, distribution)
    return {'tags': tags}

@register.inclusion_tag('attractions/cloud_for_area.html')
def cloud_for_area(area, steps=4, distribution=LOGARITHMIC):
    '''Takes an area and renders a cloud for it's attractions'''
    tags = calculate_cloud(list(tags), steps, distribution)
    return {'tags': tags}


