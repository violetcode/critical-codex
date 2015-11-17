# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('charactersheet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='weapon',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 14, 20, 7, 44, 485528), auto_now_add=True),
            preserve_default=False,
        ),
    ]
