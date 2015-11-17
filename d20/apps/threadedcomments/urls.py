from django.conf.urls import *

from site.apps.voting.views import vote_on_object

from .models import ThreadedComment
from . import views

blob_dict = {
	'model': ThreadedComment,
	'template_object_name': 'comment',
	'allow_xmlhttprequest': True,
	'post_vote_redirect': '',
	'template_name': 'aggregator/feeditem/comments.html'
}

urlpatterns = patterns('',
	url(r'^comments/posted/$', views.comment_posted, name = 'comment-redirect' ),
	url(r'^comment/(?P<id>.*)/$', views.single_comment, name='single_comment'),
)
