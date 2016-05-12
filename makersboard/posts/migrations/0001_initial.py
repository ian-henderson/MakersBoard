# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-12 15:43
from __future__ import unicode_literals

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=posts.models.upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('description', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('for_sale', models.BooleanField(default=False)),
                ('medium', models.CharField(default=None, max_length=120)),
                ('price', models.DecimalField(decimal_places=2, default=None, max_digits=10)),
            ],
            options={
                'ordering': ['-timestamp', '-updated'],
            },
        ),
    ]
