# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zombie_search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='slug',
            field=models.SlugField(unique=True),
            preserve_default=True,
        ),
    ]
