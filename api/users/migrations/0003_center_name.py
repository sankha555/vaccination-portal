# Generated by Django 3.2.5 on 2021-08-09 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_govtagency__id'),
    ]

    operations = [
        migrations.AddField(
            model_name='center',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Center Name'),
        ),
    ]
