from django.contrib import admin
from .models import CharacterSheet, Weapon, ACItem, SpellSchool, SpellEntry

# Register your models here.
class CharacterSheetAdmin(admin.ModelAdmin):
    list_display = ('name', 'player')
    ordering = ['name']

    exclude = ('slug', 'guid')

class WeaponAdmin(admin.ModelAdmin):
	list_display = ('name', 'character')
	ordering = ['character']

class ACItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'character')
	ordering = ['character']

class SpellSchoolAdmin(admin.ModelAdmin):
	list_display = ('name', 'character')
	ordering = ['character']

class SpellEntryAdmin(admin.ModelAdmin):
	list_display = ('school', 'spell', 'spell_level')
	ordering = ['school', 'spell_level']

admin.site.register(CharacterSheet, CharacterSheetAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(ACItem, ACItemAdmin)
admin.site.register(SpellSchool, SpellSchoolAdmin)
admin.site.register(SpellEntry, SpellEntryAdmin)
