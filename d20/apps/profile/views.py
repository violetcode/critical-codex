from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import cache
from django.template import RequestContext
from django.views.generic.list import ListView

from d20.apps.core.models import Account
from d20.apps.charactersheet.models import CharacterSheet, Weapon, ACItem, SpellSchool

#Main Profile View
def UserProfile(request, username):
	u = get_object_or_404(Account, username=username)
	ctx = {'user_obj': u}
	return render(request, 'profile/profile.html', ctx)

def UserCharacters(request, username):
	u = get_object_or_404(Account, username=username)
	if request.user == u:
		c = CharacterSheet.objects.filter(player__username=u.username)
	else:
		c = CharacterSheet.objects.filter(player__username=u.username).filter(is_public=True)
	ctx = {'user_obj': u, 'user_characters': c}
	return render(request, 'profile/characters.html', ctx)
