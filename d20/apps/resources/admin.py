from django.contrib import admin
from .models import Feat, SpecialAbility, Spell, CharClass, Item

# Register your models here
class ClassAdmin(admin.ModelAdmin):
	list_display = ('name', 'class_type', 'description')
	ordering = ['class_type', 'name']

class FeatAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ['name']

class SpecialAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ['name']

class SpellAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ['name']

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name',)
	ordering = ['name']

admin.site.register(CharClass, ClassAdmin)
admin.site.register(Feat, FeatAdmin)
admin.site.register(SpecialAbility, SpecialAdmin)
admin.site.register(Spell, SpecialAdmin)
admin.site.register(Item, ItemAdmin)