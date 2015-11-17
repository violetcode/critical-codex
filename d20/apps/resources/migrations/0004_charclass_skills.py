# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_charclass_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='charclass',
            name='skills',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
