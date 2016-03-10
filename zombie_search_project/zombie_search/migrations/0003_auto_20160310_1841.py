# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zombie_search', '0002_auto_20160310_1545'),
    ]

    operations = [
        migrations.RenameField(
            model_name='badge',
            old_name='name',
            new_name='type',
        ),
    ]
