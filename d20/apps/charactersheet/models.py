from datetime import datetime

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

from d20.apps.resources.models import Feat, SpecialAbility, Spell
from d20.utils.user_functions import generate_secret_token

from .managers import CharactersheetManager

MAX_LENGTH = 512

class CharacterSheet(models.Model):
    ALIGNMENT_CHOICES = (
        ('LG', 'LG'),
        ('LN', 'LN'),
        ('LE', 'LE'),
        ('NG', 'NG'),
        ('N', 'N'),
        ('NE', 'NE'),
        ('CG', 'CG'),
        ('CN', 'CN'),
        ('CE', 'CE')
    )
    SIZE_CHOICES = (
        ('-8', 'Colossal'),
        ('-4', 'Gargantuan'),
        ('-2', 'Huge'),
        ('-1', 'Large'),
        ('0', 'Medium'),
        ('1', 'Small'),
        ('2', 'Tiny'),
        ('4', 'Diminutive'),
        ('8', 'Fine')
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )



    # Attributes
    name = models.CharField(max_length=MAX_LENGTH)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='charactersheets')
    is_public = models.BooleanField(default=False)
    alignment = models.CharField(max_length=MAX_LENGTH, choices=ALIGNMENT_CHOICES, default='N')
    char_class = models.CharField(max_length=MAX_LENGTH, blank=True)
    level = models.PositiveIntegerField(default=1, null=True)
    deity = models.CharField(max_length=MAX_LENGTH, blank=True)
    homeland = models.CharField(max_length=MAX_LENGTH, blank=True)
    race = models.CharField(max_length=MAX_LENGTH, blank=True)
    gender = models.CharField(max_length=MAX_LENGTH, choices=GENDER_CHOICES, default='M')
    size = models.CharField(max_length=MAX_LENGTH, choices=SIZE_CHOICES, default='0')
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.CharField(max_length=MAX_LENGTH, blank=True)
    weight = models.CharField(max_length=MAX_LENGTH, blank=True)
    hair = models.CharField(max_length=MAX_LENGTH, blank=True)
    eyes = models.CharField(max_length=MAX_LENGTH, blank=True)
    hp_total = models.PositiveIntegerField(null=True)
    current_hp = models.IntegerField(null=True, blank=True)
    languages = models.TextField(blank=True)
    # 2 integers separated by commas in the format of
    # 'current_xp,next_level'
    xp = models.CommaSeparatedIntegerField(default='0,0', max_length=MAX_LENGTH)
    # 6 integers separated by commas in the format of
    # 'base_speed,with_armor,fly,swim,climb,burrow'
    speed = models.CommaSeparatedIntegerField(default='30,0,0,0,0,0', max_length=MAX_LENGTH)

    # Metadata
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    sheet_type = models.CharField(max_length=MAX_LENGTH, default="pathfinder")

    slug = models.SlugField(unique=True, editable=False)
    guid = models.CharField(max_length=MAX_LENGTH, unique=True, editable=False)

    #Scores
    #2 integers separated by commas in the format of:
    #'ability_score,temp_mod'
    str_score = models.CommaSeparatedIntegerField(default='10,0', max_length=MAX_LENGTH)
    dex_score = models.CommaSeparatedIntegerField(default='10,0', max_length=MAX_LENGTH)
    con_score = models.CommaSeparatedIntegerField(default='10,0', max_length=MAX_LENGTH)
    int_score = models.CommaSeparatedIntegerField(default='10,0', max_length=MAX_LENGTH)
    wis_score = models.CommaSeparatedIntegerField(default='10,0', max_length=MAX_LENGTH)
    cha_score = models.CommaSeparatedIntegerField(default='10,0', max_length=MAX_LENGTH)
    base_attack = models.PositiveIntegerField(default="0", blank=True)

    #Initiative
    init_mod = models.IntegerField(null=True, blank=True)

    #AC Stuff
    #5 integers separated by commas in the format of:
    #'armor_bonus,shield_bonus,nat_armor,deflection_mod,misc_mod'
    ac_mods = models.CommaSeparatedIntegerField(default='0,0,0,0,0', max_length=MAX_LENGTH)


    #Saves
    #4 integers separated by commas in the format of:
    #'base_save,magid_mod,misc_mod,temp_mod'
    fort_save = models.CommaSeparatedIntegerField(default='0,0,0,0', max_length=MAX_LENGTH)
    reflex_save = models.CommaSeparatedIntegerField(default='0,0,0,0', max_length=MAX_LENGTH)
    will_save = models.CommaSeparatedIntegerField(default='0,0,0,0', max_length=MAX_LENGTH)


    #Skills
    #3 integers separated by commas in the format of:
    #'class_skill,ranks,misc_mod'
    # where 1 in class_skill denotes it as a class skill, and 0 is not
    acro_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    appraise_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    bluff_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    climb_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    craft1_name= models.CharField(max_length=MAX_LENGTH, blank=True)
    craft2_name= models.CharField(max_length=MAX_LENGTH, blank=True)
    craft3_name= models.CharField(max_length=MAX_LENGTH, blank=True)
    craft1_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    craft2_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    craft3_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    diplomacy_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    disable_dev_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    disguise_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    escape_art_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    fly_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    handle_animal_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    heal_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    intimidate_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    arcana_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    dungeon_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    engineering_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    geography_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    history_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    local_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    nature_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    nobility_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    planes_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    religion_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    linguistics_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    perception_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    perform1_name= models.CharField(max_length=MAX_LENGTH, blank=True)
    perform2_name= models.CharField(max_length=MAX_LENGTH, blank=True)
    perform1_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    perform2_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    prof1_name= models.CharField(max_length=MAX_LENGTH, blank=True)
    prof2_name= models.CharField(max_length=MAX_LENGTH, blank=True)
    prof1_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    prof2_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    ride_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    sense_motive_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    sleight_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    spellcraft_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    stealth_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    survival_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    swim_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)
    use_magic_skill = models.CommaSeparatedIntegerField(default='0,0,0', max_length=MAX_LENGTH)

    #Misc
    damage_reduction = models.PositiveIntegerField(null=True, blank=True)
    spell_resist = models.PositiveIntegerField(null=True, blank=True)

    feats = models.ManyToManyField(Feat, blank=True, null=True)
    custom_feats = models.TextField(blank=True)
    special_abilities = models.ManyToManyField(SpecialAbility, blank=True, null=True)
    custom_special = models.TextField(blank=True)

    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    #Items/gear
    loot = models.TextField(blank=True)
    gear = models.TextField(blank=True)


    #Money
    #4 integers separated by commas in the format of:
    #'platinum,gold,silver,copper'
    money = models.CommaSeparatedIntegerField(default='0,0,0,0', max_length=MAX_LENGTH)

    objects = CharactersheetManager()

    def save(self, **kwargs):
        if not self.id:
            phrase = "{0} {1} {2}".format(self.player.username, self.name, datetime.now())
            self.guid = generate_secret_token(phrase)
        self.slug = "{0}-{1}".format(slugify(self.name)[:35], self.guid)
        super(CharacterSheet, self).save(**kwargs)

    def __unicode__(self):
        return self.name + " (" + self.player.username + ")"


class Weapon(models.Model):
    character = models.ForeignKey(CharacterSheet, related_name="weapons")
    name = models.CharField(max_length=MAX_LENGTH)
    attack_bonus = models.CharField(max_length=MAX_LENGTH, blank=True)
    crit_range = models.CharField(max_length=MAX_LENGTH, blank=True)
    weapon_type = models.CharField(max_length=MAX_LENGTH, blank=True)
    weapon_range = models.PositiveIntegerField(null=True, blank=True)
    ammunition = models.PositiveIntegerField(null=True, blank=True)
    damage = models.CharField(max_length=MAX_LENGTH, blank=True)
    slug = models.SlugField(unique=True, editable=False)
    guid = models.CharField(max_length=MAX_LENGTH, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        if not self.id:
            phrase = "{0} {1} {2}".format(self.character.name, self.name, datetime.now())
            self.guid = generate_secret_token(phrase)
        self.slug = "{0}-{1}".format(slugify(self.name)[:35], self.guid)
        super(Weapon, self).save(**kwargs)


    def __unicode__(self):
        return self.name + " (" + self.character.name + ")"

    class Meta:
        ordering = ('created',)

class ACItem(models.Model):
    character = models.ForeignKey(CharacterSheet, related_name="items")
    name = models.CharField(max_length=MAX_LENGTH)
    bonus = models.IntegerField(null=True)
    item_type = models.CharField(max_length=MAX_LENGTH, blank=True)
    check_penalty = models.IntegerField(null=True, blank=True)
    spell_failure = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    properties = models.CharField(max_length=MAX_LENGTH, blank=True)
    slug = models.SlugField(unique=True, editable=False)
    guid = models.CharField(max_length=MAX_LENGTH, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        if not self.id:
            phrase = "{0} {1} {2}".format(self.character.name, self.name, datetime.now())
            self.guid = generate_secret_token(phrase)
        self.slug = "{0}-{1}".format(slugify(self.name)[:35], self.guid)
        super(ACItem, self).save(**kwargs)

    def __unicode__(self):
        return self.name + " (" + self.character.name + ")"



class SpellSchool(models.Model):
    MOD_CHOICES = (
        ('wis', 'Wisdom'),
        ('int', 'Intelligence'),
        ('cha', 'Charisma')
    )
    character = models.ForeignKey(CharacterSheet, related_name="spell_schools")
    name = models.CharField(max_length=MAX_LENGTH)
    spell_mod = models.CharField(max_length=MAX_LENGTH, choices=MOD_CHOICES, default='int')

    #Spells known
    #9 integers separated by commas in the format of:
    #'0th,1st,2nd,3rd,4th,5th,6th,7th,8th,9th'
    known_spells = models.CommaSeparatedIntegerField(default='0,0,0,0,0,0,0,0,0,0', max_length=MAX_LENGTH)

    #Spells per day
    #9 integers separated by commas in the format of:
    #'0th,1st,2nd,3rd,4th,5th,6th,7th,8th,9th'
    spells_per_day = models.CommaSeparatedIntegerField(default='0,0,0,0,0,0,0,0,0,0', max_length=MAX_LENGTH)

    #Bonus spells
    #8 integers separated by commas in the format of:
    #'1st,2nd,3rd,4th,5th,6th,7th,8th,9th'
    bonus_spells = models.CommaSeparatedIntegerField(default='0,0,0,0,0,0,0,0,0', max_length=MAX_LENGTH)

    slug = models.SlugField(unique=True, editable=False)
    guid = models.CharField(max_length=MAX_LENGTH, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        if not self.id:
            phrase = "{0} {1} {2}".format(self.character.name, self.name, datetime.now())
            self.guid = generate_secret_token(phrase)
        self.slug = "{0}-{1}".format(slugify(self.name)[:35], self.guid)
        super(SpellSchool, self).save(**kwargs)

    def __unicode__(self):
        return self.name + " (" + self.character.name + ")"

class SpellEntry(models.Model):
    spell = models.ForeignKey(Spell, blank=True)
    custom_spell = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    school = models.ForeignKey(SpellSchool, related_name='spells')
    spell_level = models.PositiveIntegerField(default=0)
    prepared = models.PositiveIntegerField(default=0)
    used = models.PositiveIntegerField(default=0)
