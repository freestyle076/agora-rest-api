# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_value', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=30)),
                ('post_date_time', models.DateTimeField()),
                ('image1', models.CharField(default=b'', max_length=26, blank=True)),
                ('description', models.CharField(default=b'', max_length=1000, blank=True)),
                ('price', models.PositiveIntegerField()),
                ('isbn', models.CharField(max_length=12)),
                ('gonzaga_email', models.BooleanField(default=False)),
                ('pref_email', models.BooleanField(default=False)),
                ('phone', models.BooleanField(default=False)),
                ('image2', models.CharField(default=b'', max_length=26, blank=True)),
                ('image3', models.CharField(default=b'', max_length=26, blank=True)),
                ('username', models.ForeignKey(to='user_service.User')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DateLocationPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_value', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=30)),
                ('post_date_time', models.DateTimeField()),
                ('image1', models.CharField(default=b'', max_length=26, blank=True)),
                ('description', models.CharField(default=b'', max_length=1000, blank=True)),
                ('price', models.PositiveIntegerField()),
                ('date_time', models.DateTimeField()),
                ('location', models.CharField(max_length=20)),
                ('gonzaga_email', models.BooleanField(default=False)),
                ('pref_email', models.BooleanField(default=False)),
                ('phone', models.BooleanField(default=False)),
                ('image2', models.CharField(default=b'', max_length=26, blank=True)),
                ('image3', models.CharField(default=b'', max_length=26, blank=True)),
                ('username', models.ForeignKey(to='user_service.User')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_value', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=30)),
                ('post_date_time', models.DateTimeField()),
                ('image1', models.CharField(default=b'', max_length=26, blank=True)),
                ('description', models.CharField(default=b'', max_length=1000, blank=True)),
                ('price', models.PositiveIntegerField()),
                ('gonzaga_email', models.BooleanField(default=False)),
                ('pref_email', models.BooleanField(default=False)),
                ('phone', models.BooleanField(default=False)),
                ('image2', models.CharField(default=b'', max_length=26, blank=True)),
                ('image3', models.CharField(default=b'', max_length=26, blank=True)),
                ('username', models.ForeignKey(to='user_service.User')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RideSharePost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_value', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=30)),
                ('post_date_time', models.DateTimeField()),
                ('image1', models.CharField(default=b'', max_length=26, blank=True)),
                ('description', models.CharField(default=b'', max_length=1000, blank=True)),
                ('price', models.PositiveIntegerField()),
                ('departure_date_time', models.DateTimeField()),
                ('return_date_time', models.DateTimeField()),
                ('trip', models.CharField(max_length=50)),
                ('round_trip', models.BooleanField(default=False)),
                ('gonzaga_email', models.BooleanField(default=False)),
                ('pref_email', models.BooleanField(default=False)),
                ('phone', models.BooleanField(default=False)),
                ('image2', models.CharField(default=b'', max_length=26, blank=True)),
                ('image3', models.CharField(default=b'', max_length=26, blank=True)),
                ('username', models.ForeignKey(to='user_service.User')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
