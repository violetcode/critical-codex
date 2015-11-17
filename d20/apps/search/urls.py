from django.conf.urls import patterns, url

from haystack.query import SearchQuerySet
from haystack.views import SearchView

sqs = SearchQuerySet().order_by('-pub_date')

urlpatterns = patterns('haystack.views',
    url(r'^$', SearchView(searchqueryset=sqs), name='haystack_search'),
)