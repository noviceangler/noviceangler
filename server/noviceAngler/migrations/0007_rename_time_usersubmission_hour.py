# Generated by Django 4.0.3 on 2023-06-10 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('noviceAngler', '0006_usersubmission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersubmission',
            old_name='time',
            new_name='hour',
        ),
    ]
