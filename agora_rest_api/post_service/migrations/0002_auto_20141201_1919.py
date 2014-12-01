# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookpost',
            name='text',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datelocationpost',
            name='text',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itempost',
            name='text',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ridesharepost',
            name='text',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
