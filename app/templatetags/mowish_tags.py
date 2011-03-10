from django import template
from django.conf import settings
from mowish.app.models import *

import mowish.app.feeds.tmdb as tmdb
import mowish.app.feeds.tastekid as tastekid

register = template.Library()

@register.simple_tag
def site_url():
    return settings.SITE_URL
    
@register.filter
def cut(value, arg):
    return value[:arg]
    
@register.filter
def slug(value):
    import re
    slug = re.sub('[\W]', '-', value.strip()).replace('--','-')
    return slug
