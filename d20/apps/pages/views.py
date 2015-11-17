from __future__ import absolute_import

import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import SortedDict
from django.views.generic.list import ListView
from django.views.decorators.cache import cache_page
from django.db.models import Count
from django.core.cache import cache

from taggit.models import Tag
from mixpanel import Mixpanel

from d20.apps.core.models import Account as User
from d20.apps.charactersheet.models import CharacterSheet, Weapon, ACItem, SpellSchool
from d20.apps.resources.models import Feat, SpecialAbility, Spell

def Index(request):
	if request.user.is_authenticated():
		tpl = 'pages/index.html'
		ctx = {}
	else:
		tpl = 'pages/splash.html'
		ctx = {}
	return render(request, tpl, ctx)
