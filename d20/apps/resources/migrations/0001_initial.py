# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=512)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(unique=True, max_length=512, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('aura', models.CharField(max_length=255, null=True, blank=True)),
                ('cl', models.PositiveIntegerField(default=1, null=True, blank=True)),
                ('slot', models.PositiveIntegerField(default=b'1', max_length=2, choices=[(1, 'None'), (2, 'Belt'), (3, 'Feet'), (4, 'neck'), (5, 'shoulders'), (6, 'head'), (7, 'wrists'), (8, 'eyes'), (9, 'chest'), (10, 'headband'), (11, 'body')])),
                ('price', models.PositiveIntegerField(null=True, blank=True)),
                ('weight', models.PositiveIntegerField(null=True, blank=True)),
                ('description', models.TextField()),
                ('construction', models.TextField(null=True, blank=True)),
                ('item_type', models.PositiveIntegerField(default=b'1', max_length=2, choices=[(1, 'None'), (2, 'Weapon'), (3, 'Armor'), (5, 'Adventuring Gear'), (6, 'Special Substances and Items'), (7, 'Tools and Skill Kits'), (8, 'Clothing'), (9, 'Animal-Related Gear'), (10, 'Entertainment Items'), (11, 'Magic Item')])),
                ('destruction', models.TextField(null=True, blank=True)),
                ('game', models.ForeignKey(to='resources.GameType')),
                ('player', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpecialAbility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=512)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=512)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
