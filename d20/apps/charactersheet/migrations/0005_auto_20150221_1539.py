# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charactersheet', '0004_auto_20150221_1539'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weapon',
            options={'ordering': ('created',)},
        ),
    ]
