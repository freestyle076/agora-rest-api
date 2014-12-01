# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=40)),
                ('gonzaga_email', models.EmailField(unique=True, max_length=75)),
                ('pref_email', models.EmailField(max_length=75, null=True, blank=True)),
                ('phone', models.CharField(max_length=11, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
