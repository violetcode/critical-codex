# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charactersheet', '0008_auto_20150318_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charactersheet',
            name='custom_spells',
        ),
    ]
