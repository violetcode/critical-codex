# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resources', '0002_auto_20150210_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='charclass',
            name='player',
            field=models.ForeignKey(related_name='custom_classes', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
