# Generated by Django 4.2.1 on 2023-05-25 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0002_rename_number_room_room_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='room_name',
            new_name='name',
        ),
    ]
