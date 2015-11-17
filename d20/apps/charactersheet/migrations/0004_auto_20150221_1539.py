# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charactersheet', '0003_auto_20150221_1441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weapon',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='charactersheet',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='charactersheet',
            name='gear',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='charactersheet',
            name='notes',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
