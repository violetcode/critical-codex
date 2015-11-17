from __future__ import absolute_import
import hashlib
from urlparse import urlparse

from django.shortcuts import redirect, render, get_object_or_404
from django import template

from d20.apps.core.models import Account
from ..models import CharacterSheet

register = template.Library()

@register.inclusion_tag('charactersheet/templatetags/render_characters.html')
def render_pub_characters(user, num=25):
	objects = CharacterSheet.objects.public().filter(player__username=user)[:num]
	return { 'objects': objects}

@register.inclusion_tag('charactersheet/templatetags/render_characters.html')
def render_all_characters(user, num=25):
	objects = CharacterSheet.objects.filter(player__username=user)[:num]
	return { 'objects': objects}
