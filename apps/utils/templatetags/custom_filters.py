#!/usr/bin/env python
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter
def truncatestring (value, arg):
    try:
        length = int(arg)
    except ValueError: 
        return value # Fail silently.
    
    text = force_unicode(value)
    out = text[:length]
    
    if len(text) > len(out):
        out += "&hellip;"
    
    return mark_safe(out)
