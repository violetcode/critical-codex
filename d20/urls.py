from django.conf.urls import patterns, include, url
from django.contrib.sitemaps import Sitemap, GenericSitemap
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static

from d20.apps.core import views as core_views

admin.autodiscover()

urlpatterns = patterns('',

	#admin
	url(r'^admin42/', include(admin.site.urls)),

	#Apps
	url(r'^api/', include('d20.apps.api.urls', namespace='API', app_name='d20_api')),
	url(r'^characters/', include('d20.apps.charactersheet.urls', namespace='Charactersheet', app_name='d20_charactersheets')),
	url(r'^profile/', include('d20.apps.profile.urls', namespace='Profile', app_name='d20_profile')),
	url(r'^search/', include('d20.apps.search.urls', namespace='Search',)),
	url(r'zebra/', include('zebra.urls', namespace="zebra",  app_name='zebra')),
	url(r'^', include('d20.apps.pages.urls', namespace='Pages', app_name='d20_pages')),
	url(r'^', include('d20.apps.core.urls', namespace='Core', app_name='d20_core')),

	# Error Pages
	url(r'^404/$', TemplateView.as_view(template_name="404.html"), name='error-404'),
	url(r'^500/$', TemplateView.as_view(template_name="500.html"), name='error-500'),

	#Static
	url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
	url(r'^humans\.txt$', TemplateView.as_view(template_name="humans.txt", content_type='text/plain')),

	url(r'^about/$', TemplateView.as_view(template_name="pages/about.html"), name='static-about'),
	url(r'^terms/$', TemplateView.as_view(template_name="pages/terms.html"), name='static-terms'),
	url(r'^terms/billing/$', TemplateView.as_view(template_name="pages/billing.html"), name='static-billing'),
	url(r'^privacy/$', TemplateView.as_view(template_name="pages/privacy.html"), name='static-privacy'),
	url(r'^dmca/$', TemplateView.as_view(template_name="pages/dmca.html"), name='static-dmca'),
	url(r'^tour/$', TemplateView.as_view(template_name="pages/tour.html"), name='static-tour'),
	url(r'^faq/$', TemplateView.as_view(template_name="pages/faq.html"), name='static-faq'),
	url(r'^splash/$', TemplateView.as_view(template_name="pages/splash.html"), name='static-splash'),
	url(r'^popup/$', TemplateView.as_view(template_name="includes/popup.html"), name='popup'),
)

if settings.DEBUG:
	#Static Media
	urlpatterns += patterns('',
	    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
	        'document_root': settings.STATIC_ROOT,
	    }),
	)
