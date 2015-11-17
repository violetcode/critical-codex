from __future__ import absolute_import

from django.conf.urls import *
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',
	url(r'^new/$', TemplateView.as_view(template_name='charactersheet/angular/manage.html'), name="Charactersheet-New"),
	#url(r'^(?P<slug>[-\w]+)/$', views.CharactersheetDetail, name = "Charactersheet-Detail"),
	#url(r'^(?P<slug>[-\w]+)/edit/$', TemplateView.as_view(template_name='charactersheet/angular/edit.html'), name="Charactersheet-Edit"),
	url(r'^(?P<slug>[-\w]+)/$', TemplateView.as_view(template_name='charactersheet/angular/edit.html'), name="Charactersheet-Detail"),
	url(r'^$', views.CharactersheetListView.as_view(), name = "Charactersheet-List"),

)
