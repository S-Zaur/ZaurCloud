import hashlib

from django import template

register = template.Library()


@register.simple_tag
def hasher(value):
    return hashlib.md5(value.encode()).hexdigest()[:12]


register.filter("hasher", hasher)
