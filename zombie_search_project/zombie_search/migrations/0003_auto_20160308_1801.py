# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zombie_search', '0002_auto_20160308_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='profile_picture',
            field=models.ImageField(upload_to=b'', blank=True),
        ),
    ]
