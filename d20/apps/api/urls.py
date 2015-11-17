from __future__ import absolute_import

from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .views.user import *
from .views.resources import *
from .views.charactersheet import *


urlpatterns = patterns('',

    #Users
    url(r'^users/(?P<username>[0-9a-zA-Z_-]+)/charactersheets$', UserCharacterSheetList.as_view(), name='userCharacterSheet-list'),
    url(r'^users/(?P<username>[0-9a-zA-Z_-]+)$', UserDetail.as_view(), name='user-detail'),
    url(r'^users$', UserList.as_view(), name='user-list'),

    url(r'^current$', CurrentUser.as_view(), name='user-current'),

    #Resources
    url(r'^resources/abilities$', SpecialAbilitiesList.as_view(), name='resourcesSpecialAbilities-list'),
    url(r'^resources/spells$', SpellsList.as_view(), name='resourcesSpells-list'),
    url(r'^resources/feats$', FeatsList.as_view(), name='resourcesFeats-list'),
    url(r'^resources/$', TemplateView.as_view(template_name="api/resources.html"), name='API-Resources'),

    #CharacterSheet
    url(r'^characters/create$', CharacterCreate.as_view(), name='charactersheet-create'),
    url(r'^characters/(?P<slug>[0-9a-zA-Z_-]+)$', CharacterSheetDetail.as_view(), name='charactersheet-detail'),
    url(r'^characters/$', CharacterSheetList.as_view(), name='charactersheet-list'),

    url(r'^weapons/create$', WeaponCreate.as_view(), name="weapon-create"),
    url(r'^weapons/(?P<slug>[0-9a-zA-Z_-]+)$', WeaponDetail.as_view(), name="weapon-detail"),

    url(r'^spellschool/create$', SpellSchoolCreate.as_view(), name="spellschool-create"),
    url(r'^spellschool/(?P<slug>[0-9a-zA-Z_-]+)$', SpellSchoolDetail.as_view(), name="spellschool-detail"),

    url(r'^spell/create$', SpellEntryCreate.as_view(), name="spellentry-create"),
    url(r'^spell/(?P<pk>[0-9]+)$', SpellEntryDetail.as_view(), name="spellentry-detail"),

    #Static
    url(r'^$', TemplateView.as_view(template_name="api/index.html"), name='API-Index'),
)
