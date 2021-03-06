# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-07 08:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_books'),
    ]

    operations = [
        migrations.CreateModel(
            name='receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'Available'), ('PB', 'Pre-booked'), ('I', 'Issued')], default='A', max_length=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='books',
            name='current_sub',
        ),
        migrations.AddField(
            model_name='receipt',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.books'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.subscriber'),
        ),
    ]
