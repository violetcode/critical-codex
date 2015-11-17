# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_charclass_skills'),
        ('charactersheet', '0007_spellschool_custom_spells'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpellEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('custom_spell', models.CharField(max_length=512, null=True, blank=True)),
                ('spell_level', models.PositiveIntegerField(default=0)),
                ('prepared', models.PositiveIntegerField(default=0)),
                ('used', models.PositiveIntegerField(default=0)),
                ('school', models.ForeignKey(related_name='spells', to='charactersheet.SpellSchool')),
                ('spell', models.ForeignKey(to='resources.Spell', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='spellschool',
            name='custom_spells',
        ),
        migrations.RemoveField(
            model_name='spellschool',
            name='spells_0',
        ),
        migrations.RemoveField(
            model_name='spellschool',
            name='spells_1',
        ),
        migrations.RemoveField(
            model_name='spellschool',
            name='spells_2',
        ),
        migrations.RemoveField(
            model_name='spellschool',
            name='spells_3',
        ),
        migrations.RemoveField(
            model_name='spellschool',
            name='spells_4',
        ),
        migrations.RemoveField(
            model_name='spellschool',
            name='spells_5',
        ),
        migrations.RemoveField(
            model_name='spellschool',
            name='spells_6',
        ),
        migrations.RemoveField(
            model_name='spellschool',
            name='spells_7',
        ),
        migrations.RemoveField(
            model_name='spellschool',
            name='spells_8',
        ),
        migrations.RemoveField(
            model_name='spellschool',
            name='spells_9',
        ),
    ]
