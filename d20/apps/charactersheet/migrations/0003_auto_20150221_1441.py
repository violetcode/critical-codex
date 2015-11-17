# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_charclass_skills'),
        ('charactersheet', '0002_weapon_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weapon',
            options={'ordering': ('created',)},
        ),
        migrations.RemoveField(
            model_name='spellschool',
            name='spells',
        ),
        migrations.AddField(
            model_name='acitem',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 21, 14, 40, 6, 102254), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='acitem',
            name='guid',
            field=models.CharField(default=datetime.datetime(2015, 2, 21, 14, 40, 26, 926093), unique=True, max_length=512, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='acitem',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2015, 2, 21, 14, 40, 42, 118014), unique=True, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 21, 14, 40, 49, 853719), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='guid',
            field=models.CharField(default=datetime.datetime(2015, 2, 21, 14, 40, 56, 725796), unique=True, max_length=512, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2015, 2, 21, 14, 41, 3, 749585), unique=True, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='spells_0',
            field=models.ManyToManyField(related_name='0_level_spells', to='resources.Spell', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='spells_1',
            field=models.ManyToManyField(related_name='1_level_spells', to='resources.Spell', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='spells_2',
            field=models.ManyToManyField(related_name='2_level_spells', to='resources.Spell', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='spells_3',
            field=models.ManyToManyField(related_name='3_level_spells', to='resources.Spell', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='spells_4',
            field=models.ManyToManyField(related_name='4_level_spells', to='resources.Spell', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='spells_5',
            field=models.ManyToManyField(related_name='5_level_spells', to='resources.Spell', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='spells_6',
            field=models.ManyToManyField(related_name='6_level_spells', to='resources.Spell', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='spells_7',
            field=models.ManyToManyField(related_name='7_level_spells', to='resources.Spell', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='spells_8',
            field=models.ManyToManyField(related_name='8_level_spells', to='resources.Spell', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spellschool',
            name='spells_9',
            field=models.ManyToManyField(related_name='9_level_spells', to='resources.Spell', blank=True),
            preserve_default=True,
        ),
    ]
