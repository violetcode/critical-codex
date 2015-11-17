# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charactersheet', '0009_remove_charactersheet_custom_spells'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acitem',
            name='character',
            field=models.ForeignKey(related_name='items', blank=True, to='charactersheet.CharacterSheet', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='charactersheet',
            name='feats',
            field=models.ManyToManyField(to='resources.Feat', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='charactersheet',
            name='special_abilities',
            field=models.ManyToManyField(to='resources.SpecialAbility', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spellschool',
            name='character',
            field=models.ForeignKey(related_name='spell_schools', blank=True, to='charactersheet.CharacterSheet', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weapon',
            name='character',
            field=models.ForeignKey(related_name='weapons', blank=True, to='charactersheet.CharacterSheet', null=True),
            preserve_default=True,
        ),
    ]
