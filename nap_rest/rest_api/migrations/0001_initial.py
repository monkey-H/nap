# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('ip', models.GenericIPAddressField()),
                ('port', models.PositiveSmallIntegerField(default=0)),
                ('cat', models.TextField()),
                ('state', models.CharField(max_length=100)),
                ('sub', models.CharField(max_length=100)),
                ('journal', models.TextField()),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('origin_url', models.CharField(max_length=200)),
                ('instance_num', models.PositiveSmallIntegerField(default=0)),
                ('owner', models.ForeignKey(related_name='services', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='app',
            name='service',
            field=models.ForeignKey(related_name='app', to='rest_api.Service'),
        ),
    ]
