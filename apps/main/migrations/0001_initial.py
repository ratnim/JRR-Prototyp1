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
            name='Expert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('trained', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(verbose_name='First Name', max_length=256)),
                ('last_name', models.CharField(verbose_name='Last Name', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('passed', models.BooleanField(verbose_name='Passed Course', default=False)),
                ('available', models.BooleanField(verbose_name='Is available', default=True)),
            ],
        ),
        migrations.AddField(
            model_name='expert',
            name='profile',
            field=models.OneToOneField(to='main.Profile'),
        ),
        migrations.AddField(
            model_name='expert',
            name='status',
            field=models.OneToOneField(to='main.Status'),
        ),
        migrations.AddField(
            model_name='expert',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
