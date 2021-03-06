# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-26 15:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('contract', models.FileField(blank=True, null=True, upload_to='documents/', verbose_name='file')),
                ('is_superuser', models.BooleanField(default=True, verbose_name='is superuser')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='last name')),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_issues', to='app.User', verbose_name='created by'),
        ),
        migrations.AddField(
            model_name='issue',
            name='leader',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='leading_issue', to='app.User', verbose_name='leader'),
        ),
        migrations.AddField(
            model_name='issue',
            name='solver',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solving_issue', to='app.User', verbose_name='solver'),
        ),
        migrations.AddField(
            model_name='issue',
            name='watched_by',
            field=models.ManyToManyField(blank=True, related_name='watched_issues', to='app.User', verbose_name='watched by'),
        ),
    ]
