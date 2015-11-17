import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from taggit.managers import TaggableManager
from d20.utils.user_functions import generate_secret_token

MAX_LENGTH = 512

SLOT_CHOICES = (
	(1, _('None')),
	(2, _('Belt')),
	(3, _('Feet')),
    (4, _('neck')),
    (5, _('shoulders')),
    (6, _('head')),
    (7, _('wrists')),
    (8, _('eyes')),
    (9, _('chest')),
    (10, _('headband')),
    (11, _('body')),
)

ITEM_TYPE_CHOICES = (
    (1, _('None')),
	(2, _('Weapon')),
    (3, _('Armor')),
	(5, _('Adventuring Gear')),
	(6, _('Special Substances and Items')),
    (7, _('Tools and Skill Kits')),
    (8, _('Clothing')),
    (9, _('Animal-Related Gear')),
    (10, _('Entertainment Items')),
    (11, _('Magic Item')),
)

SP_ABIL_CHOICES = (
    ('EX', _('EX')),
    ('SP', _('SP')),
    ('SU', _('SU')),
    ('NA', _('NA'))
)

CLASS_TYPES = (
    ('Core', _('Core')),
    ('Advanced', _('Advanced')),
    ('Prestige', _('Prestige')),
)

DEFAULT_USER_ID = 1

# Create your models here.
class CharClass(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    description = models.TextField()
    alignment_req = models.CharField(max_length=MAX_LENGTH, blank=True)
    hit_die = models.CharField(max_length=MAX_LENGTH)
    skills = models.TextField(blank=True)
    wealth = models.CharField(max_length=MAX_LENGTH, blank=True)
    class_type = models.CharField(max_length=MAX_LENGTH, choices=CLASS_TYPES, default="Core")
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='custom_classes', default=DEFAULT_USER_ID)

    def __unicode__(self):
        return self.name

class Feat(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class SpecialAbility(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    abil_type = models.CharField(max_length=MAX_LENGTH, choices=SP_ABIL_CHOICES, default="NA")
    description = models.TextField()
    class_req = models.ManyToManyField(CharClass, related_name='special_abils', null=True)

    def __unicode__(self):
        return self.name

class Spell(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class GameType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(GameType, self).save(*args, **kwargs)

class Item(models.Model):
    guid = models.CharField(max_length=MAX_LENGTH, unique=True, editable=False)
    name = models.CharField(max_length=255)
    aura = models.CharField(max_length=255, blank=True, null=True)
    cl = models.PositiveIntegerField(default=1, blank=True, null=True)
    slot = models.PositiveIntegerField(max_length=2, choices=SLOT_CHOICES, default='1')
    price = models.PositiveIntegerField(blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField()
    construction = models.TextField(blank=True, null=True)
    item_type = models.PositiveIntegerField(max_length=2, choices=ITEM_TYPE_CHOICES, default='1')
    destruction = models.TextField(blank=True, null=True)
    player = models.ForeignKey(settings.AUTH_USER_MODEL)
    game = models.ForeignKey(GameType)
    tags = TaggableManager()

    def save(self, **kwargs):
        if not self.id:
            phrase = "{0} {1} {2}".format(self.player.username, self.name, datetime.now())
            self.guid = generate_secret_token(phrase)
        super(Item, self).save(**kwargs)

    def __unicode__(self):
        return self.name
