# Generated by Django 4.1.2 on 2022-10-29 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_data',
            new_name='event_date',
        ),
    ]