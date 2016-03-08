# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_awarded', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=20)),
                ('criteria', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('icon', models.ImageField(upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('password', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=20)),
                ('profile_picture', models.ImageField(upload_to=b'')),
                ('games_played', models.IntegerField(default=0)),
                ('most_days_survived', models.IntegerField(default=0)),
                ('most_kills', models.IntegerField(default=0)),
                ('most_people', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='achievement',
            name='badge',
            field=models.ForeignKey(to='zombie_search.Badge'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='achievement',
            name='player',
            field=models.ForeignKey(to='zombie_search.Player'),
            preserve_default=True,
        ),
    ]
