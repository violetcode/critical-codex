import datetime
import re
import random
import time
import logging
import operator

from django.http import HttpResponse
from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.db.models import Q


from .models import Account
from .utils import get_domain, get_ip

#from site.utils import log as logging

logger = logging.getLogger(__name__)
lower = operator.methodcaller('lower')

UNSET = object()

class SetRemoteAddrFromForwardedFor(object):
    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            pass
        else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.
            # Take just the first one.
            real_ip = real_ip.split(",")[0]
            request.META['REMOTE_ADDR'] = real_ip


class MultipleProxyMiddleware(object):
    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
    ]

    def process_request(self, request):
        """
        Rewrites the proxy headers so that only the most
        recent proxy is used.
        """
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if ',' in request.META[field]:
                    parts = request.META[field].split(',')
                    request.META[field] = parts[-1].strip()

class LastSeenMiddleware(object):
    def process_response(self, request, response):
        if ((request.path == 'clear/' or
             request.path.startswith('recent/'))
            and hasattr(request, 'user')
            and request.user.is_authenticated()):
            hour_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=60)
            ip = request.META.get('HTTP_X_REAL_IP', None) or request.META['REMOTE_ADDR']

            #if request.user.last_seen_on < hour_ago:
            #    logging.user(request, "~FG~BBRepeat visitor: ~SB%s (%s)" % (
            #        request.user.last_seen_on, ip))
            #elif settings.DEBUG:
            #    logging.user(request, "~FG~BBRepeat visitor (ignored): ~SB%s (%s)" % (
            #        request.user.last_seen_on, ip))

            request.user.last_seen_on = datetime.datetime.now()
            request.user.last_seen_ip = ip
            request.user.save()

        return response

class TimingMiddleware:
    def process_request(self, request):
        setattr(request, 'start_time', time.time())


class SubdomainMiddleware(object):
    """
    A middleware class that adds a ``subdomain`` attribute to the current request.
    """
    def get_domain_for_request(self, request):
        """
        Returns the domain that will be used to identify the subdomain part
        for this request.
        """
        return get_domain()

    def process_request(self, request):
        """
        Adds a ``subdomain`` attribute to the ``request`` parameter.
        """
        domain, host = map(lower,
            (self.get_domain_for_request(request), request.get_host()))

        pattern = r'^(?:(?P<subdomain>.*?)\.)?%s(?::.*)?$' % re.escape(domain)
        matches = re.match(pattern, host)

        if matches:
            request.subdomain = matches.group('subdomain')
        else:
            request.subdomain = None
            logger.warning('The host %s does not belong to the domain %s, '
                'unable to identify the subdomain for this request',
                request.get_host(), domain)



class SubdomainURLRoutingMiddleware(SubdomainMiddleware):
    """
    A middleware class that allows for subdomain-based URL routing.
    """
    def process_request(self, request):
        """
        Sets the current request's ``urlconf`` attribute to the urlconf
        associated with the subdomain, if it is listed in
        ``settings.SUBDOMAIN_URLCONFS``.
        """
        super(SubdomainURLRoutingMiddleware, self).process_request(request)

        subdomain = getattr(request, 'subdomain', UNSET)

        if subdomain is not UNSET:
            urlconf = settings.SUBDOMAIN_URLCONFS.get(subdomain)
            if urlconf is not None:
                logger.debug("Using urlconf %s for subdomain: %s",
                    repr(urlconf), repr(subdomain))
                request.urlconf = urlconf

    def process_response(self, request, response):
        """
        Forces the HTTP ``Vary`` header onto requests to avoid having responses
        cached across subdomains.
        """
        if getattr(settings, 'FORCE_VARY_ON_HOST', True):
            patch_vary_headers(response, ('Host',))

        return response
