# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charactersheet', '0010_auto_20150324_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acitem',
            name='character',
            field=models.ForeignKey(related_name='items', to='charactersheet.CharacterSheet'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spellschool',
            name='character',
            field=models.ForeignKey(related_name='spell_schools', to='charactersheet.CharacterSheet'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weapon',
            name='character',
            field=models.ForeignKey(related_name='weapons', to='charactersheet.CharacterSheet'),
            preserve_default=True,
        ),
    ]
