# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charactersheet', '0005_auto_20150221_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spellschool',
            name='bonus_spells',
            field=models.CommaSeparatedIntegerField(default=b'0,0,0,0,0,0,0,0,0', max_length=512),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spellschool',
            name='known_spells',
            field=models.CommaSeparatedIntegerField(default=b'0,0,0,0,0,0,0,0,0,0', max_length=512),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spellschool',
            name='spells_per_day',
            field=models.CommaSeparatedIntegerField(default=b'0,0,0,0,0,0,0,0,0,0', max_length=512),
            preserve_default=True,
        ),
    ]
