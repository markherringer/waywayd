from django import http
from django.conf import settings
from django.utils import importlib
from django.utils.translation import check_for_language, activate, to_locale, get_language
from django.utils.text import javascript_quote
import os
import gettext as gettext_module

def setlang(request):
    """
    Redirect to a given url while setting the chosen language in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    next = request.REQUEST.get('next', None)
    lang_code = request.POST.get('language', None)

    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next or next=='/':
        next = '/%s/' % lang_code

    if next[1:3] in ['it', 'en'] and next[1:3] != lang_code:
        next = next[0]+lang_code+next[3:]
    elif next[1:12] == 'attractions':
        next = next[0]+lang_code+next

    response = http.HttpResponseRedirect(next)
    if request.method == 'POST':
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response

from attractions.models import Feedback

def feedback_form(request):
    try:
        f = Feedback(name=request.POST.get('name'), email=request.POST.get('email'), message=request.POST.get('message'))
        f.save()
    except:
        return http.HttpResponse("Who knows?")

    return http.HttpResponse("OK")
