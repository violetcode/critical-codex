# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charactersheet', '0006_auto_20150221_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='spellschool',
            name='custom_spells',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
