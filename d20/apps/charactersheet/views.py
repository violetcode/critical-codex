from __future__ import absolute_import

import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Q

from taggit.models import Tag
from mixpanel import Mixpanel

from d20.apps.core.models import Account as User
from d20.apps.resources.models import Feat, SpecialAbility, Spell
from .models import CharacterSheet, Weapon, ACItem, SpellSchool

class SimpleStaticView(TemplateView):
    def get_template_names(self):
        return "charactersheet/angular/%s.html" % (self.kwargs.get('template_name'))

    def get(self, request, *args, **kwargs):
        return super(SimpleStaticView, self).get(request, *args, **kwargs)

#All Public charactersheets
class CharactersheetListView(ListView):
    paginate_by = 25
    template_name = 'charactersheet/list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            charsheets = CharacterSheet.objects.filter(
                Q(is_public=True) |
                Q(player__username=request_user.username)
            )
            return charsheets
        else:
            charsheets = CharacterSheet.objects.filter(is_public=True)
            return charsheets

    def get_context_data(self, **kwargs):
        context = super(CharactersheetListView, self).get_context_data(**kwargs)
        context.update({ 'head_title': 'Public Characters', })
        return context

#Charactersheet
def CharactersheetDetail(request, slug):
    charsheet = get_object_or_404(CharacterSheet, slug=slug)
    if charsheet.is_public or request.user.username == charsheet.player.username:
        template = ['charactersheet/characters/%s.html' % charsheet.slug, 'charactersheet/charactersheet_detail.html']
        variables = RequestContext(request, {'object': charsheet,})
    else:
        template = ['404.html',]
        variables = RequestContext(request, {})
    return render_to_response(template, variables)
