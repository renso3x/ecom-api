# Generated by Django 3.0.7 on 2020-06-25 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200625_0720'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='addresses',
            new_name='address',
        ),
    ]
