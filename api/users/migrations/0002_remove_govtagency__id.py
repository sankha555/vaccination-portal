# Generated by Django 3.2.5 on 2021-08-09 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='govtagency',
            name='_id',
        ),
    ]
