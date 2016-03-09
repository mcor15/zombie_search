# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zombie_search', '0003_auto_20160308_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='total_kills',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
