import struct
import hashlib
import datetime

from django.contrib.sites.models import Site
from django.conf import settings
from django import template
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from urlparse import urlparse
from django.shortcuts import redirect, render, get_object_or_404

from d20.apps.core.models import Account


register = template.Library()

@register.simple_tag
def current_domain(dev=False, strip_www=False):
    current_site = Site.objects.get_current()
    domain = current_site and current_site.domain
    if dev and settings.SERVER_NAME in ["dev"] and domain:
        domain = domain.replace("www", "dev")
    if strip_www:
        domain = domain.replace("www.", "")
    return domain

@register.filter
def base_site_url(value):
	parsed = urlparse(value)
	return parsed.netloc

@register.filter
def email_hash(value):
	u = get_object_or_404(Account, username=value)
	a = hashlib.md5(u.email).hexdigest()
	return a
