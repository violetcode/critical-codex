# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=512)),
                ('description', models.TextField()),
                ('alignment_req', models.CharField(max_length=512, blank=True)),
                ('hit_die', models.CharField(max_length=512)),
                ('wealth', models.CharField(max_length=512, blank=True)),
                ('class_type', models.CharField(default=b'Core', max_length=512, choices=[(b'Core', 'Core'), (b'Advanced', 'Advanced'), (b'Prestige', 'Prestige')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='specialability',
            name='abil_type',
            field=models.CharField(default=b'NA', max_length=512, choices=[(b'EX', 'EX'), (b'SP', 'SP'), (b'SU', 'SU'), (b'NA', 'NA')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='specialability',
            name='class_req',
            field=models.ManyToManyField(related_name='special_abils', null=True, to='resources.CharClass'),
            preserve_default=True,
        ),
    ]
