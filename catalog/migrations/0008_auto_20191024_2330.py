# Generated by Django 2.2.6 on 2019-10-25 03:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20191024_2244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': (('can_manage', 'Manage Books'),)},
        ),
    ]
