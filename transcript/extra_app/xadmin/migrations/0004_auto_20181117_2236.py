# Generated by Django 2.0.3 on 2018-11-18 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xadmin', '0003_auto_20160715_0100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmark',
            old_name='all_user',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='log',
            old_name='all_user',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='usersettings',
            old_name='all_user',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='userwidget',
            old_name='all_user',
            new_name='user',
        ),
    ]
