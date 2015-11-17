from rest_framework import serializers

from d20.apps.core.models import Account
from d20.apps.charactersheet.models import CharacterSheet, Weapon, ACItem, SpellSchool, SpellEntry
from d20.apps.resources.models import Feat, SpecialAbility, Spell


#Resources
class FeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feat
        fields = ('id', 'name', 'description')

class SpecialAbilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecialAbility
        fields = ('id', 'name', 'description')

class SpellSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spell
        fields = ('id', 'name', 'description')

#Charactersheets
class WeaponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weapon
        fields = ('slug', 'name', 'character', 'attack_bonus', 'crit_range', 'weapon_type',
            'weapon_range', 'ammunition', 'damage')

class ACItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ACItem
        fields = ('name', 'bonus', 'item_type', 'check_penalty', 'spell_failure',
            'weight', 'properties')

class SpellEntrySerializer(serializers.ModelSerializer):
    spell = serializers.SlugRelatedField(slug_field="name", queryset=Spell.objects.all())
    school = serializers.PrimaryKeyRelatedField(queryset=SpellSchool.objects.all())

    class Meta:
        model = SpellEntry
        fields = ('id', 'spell', 'custom_spell', 'spell_level', 'prepared', 'used', 'school')

class SpellSchoolSerializer(serializers.ModelSerializer):
    spells = SpellEntrySerializer(many=True, read_only=True)
    
    class Meta:
        model = SpellSchool
        fields = ('id', 'name', 'character', 'slug', 'spell_mod', 'known_spells', 'spells_per_day', 'bonus_spells', 
            'spells')

class CharacterSheetSerializer(serializers.HyperlinkedModelSerializer):
    player = serializers.ReadOnlyField(source='player.username')
    weapons = serializers.SlugRelatedField(many=True, slug_field="slug", queryset=Weapon.objects.all(), required=False)
    items = serializers.SlugRelatedField(many=True, slug_field="slug", queryset=ACItem.objects.all(), required=False)
    spell_schools = serializers.SlugRelatedField(many=True, slug_field="slug", queryset=SpellSchool.objects.all(), required=False)

    feats = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Feat.objects.all(), required=False)
    special_abilities = SpecialAbilitySerializer(many=True, required=False)

    class Meta:
        model = CharacterSheet
        fields = ('id', 'name', 'player', 'slug', 'guid', 'created', 'last_updated',
            'sheet_type', 'alignment', 'char_class', 'is_public',
            'level', 'deity', 'homeland', 'race', 'gender', 'size', 'age', 'height',
            'weight', 'hair','eyes', 'hp_total', 'current_hp', 'speed', 'languages',
            'xp', 'str_score', 'dex_score', 'con_score', 'int_score', 'wis_score',
            'cha_score', 'base_attack', 'init_mod', 'ac_mods', 'fort_save', 'reflex_save',
            'will_save', 'acro_skill', 'appraise_skill', 'bluff_skill', 'climb_skill',
            'craft1_name', 'craft1_skill', 'craft2_name', 'craft2_skill', 'craft3_name',
            'craft3_skill', 'diplomacy_skill', 'disable_dev_skill', 'disguise_skill',
            'escape_art_skill', 'fly_skill', 'handle_animal_skill', 'heal_skill',
            'intimidate_skill', 'arcana_skill', 'dungeon_skill', 'engineering_skill',
            'geography_skill', 'history_skill', 'local_skill', 'nature_skill', 'nobility_skill',
            'planes_skill', 'religion_skill', 'linguistics_skill', 'perception_skill',
            'perform1_name', 'perform1_skill', 'perform2_name', 'perform2_skill',
            'prof1_name', 'prof1_skill', 'prof2_name', 'prof2_skill', 'ride_skill',
            'sense_motive_skill', 'sleight_skill', 'spellcraft_skill', 'stealth_skill',
            'survival_skill', 'swim_skill', 'use_magic_skill', 'damage_reduction',
            'spell_resist', 'loot', 'money', 'weapons', 'items', 'spell_schools',
            'special_abilities', 'feats', 'custom_feats', 'custom_special', 
            'description', 'notes', 'gear')


class CharacterSheetSerializerSimple(serializers.HyperlinkedModelSerializer):
    player = serializers.ReadOnlyField(source='player.username')
    url = serializers.HyperlinkedIdentityField(view_name='charactersheet-detail', lookup_field='slug')

    class Meta:
        model = CharacterSheet
        fields = ('guid', 'name', 'player', 'url', 'slug', 'last_updated')

#Users
class UserSerializer(serializers.HyperlinkedModelSerializer):
    #charactersheets = CharacterSheetSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name', )
