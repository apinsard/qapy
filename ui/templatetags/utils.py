# -*- coding: utf-8 -*-
from django.template import Library


register = Library()


@register.simple_tag
def url_replace(request, field, value):
    querystring = request.GET.copy()
    querystring[field] = value
    return "?{}".format(querystring.urlencode())
