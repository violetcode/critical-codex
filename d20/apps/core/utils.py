import functools
import re
from urlparse import urlunparse

from django.conf import settings
from django.core.urlresolvers import reverse as simple_reverse


IP_RE = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

def get_ip(request):
    # if neither header contain a value, just use local loopback
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        # make sure we have one and only one IP
        try:
            ip_address = IP_RE.match(ip_address)
            if ip_address:
                ip_address = ip_address.group(0)
            else:
                # no IP, probably from some dirty proxy or other device
                # throw in some bogus IP
                ip_address = '10.0.0.1'
        except IndexError:
            pass

    return ip_address

def current_domain():
    from django.contrib.sites.models import Site
    return Site.objects.get_current().domain


def current_site_domain():
    domain = getattr(settings, 'SUBDOMAINS_DOMAIN', current_domain)()
    prefix = 'www.'
    if getattr(settings, 'REMOVE_WWW_FROM_DOMAIN', False) \
            and domain.startswith(prefix):
        domain = domain.replace(prefix, '', 1)

    return domain

get_domain = current_site_domain


def urljoin(domain, path=None, scheme=None):
    """
    Joins a domain, path and scheme part together, returning a full URL.

    :param domain: the domain, e.g. ``example.com``
    :param path: the path part of the URL, e.g. ``/example/``
    :param scheme: the scheme part of the URL, e.g. ``http``, defaulting to the
        value of ``settings.DEFAULT_URL_SCHEME``
    :returns: a full URL
    """
    if scheme is None:
        scheme = getattr(settings, 'DEFAULT_URL_SCHEME', 'http')

    return urlunparse((scheme, domain, path or '', None, None, None))


def reverse(viewname, subdomain=None, scheme=None, args=None, kwargs=None,
        current_app=None):
    """
    Reverses a URL from the given parameters, in a similar fashion to
    :meth:`django.core.urlresolvers.reverse`.

    :param viewname: the name of URL
    :param subdomain: the subdomain to use for URL reversing
    :param scheme: the scheme to use when generating the full URL
    :param args: positional arguments used for URL reversing
    :param kwargs: named arguments used for URL reversing
    :param current_app: hint for the currently executing application
    """
    urlconf = settings.SUBDOMAIN_URLCONFS.get(subdomain, settings.ROOT_URLCONF)

    domain = get_domain()
    if subdomain is not None:
        domain = '%s.%s' % (subdomain, domain)

    path = simple_reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs,
        current_app=current_app)
    return urljoin(domain, path, scheme=scheme)


#: :func:`reverse` bound to insecure (non-HTTPS) URLs scheme
insecure_reverse = functools.partial(reverse, scheme='http')

#: :func:`reverse` bound to secure (HTTPS) URLs scheme
secure_reverse = functools.partial(reverse, scheme='https')

#: :func:`reverse` bound to be relative to the current scheme
relative_reverse = functools.partial(reverse, scheme='')
