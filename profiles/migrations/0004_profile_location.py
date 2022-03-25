# Generated by Django 3.1.1 on 2021-12-09 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_remove_profile_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.IntegerField(choices=[(0, 'SET LATER'), (1, 'KUTUS'), (2, 'KERUGOYA'), (3, 'KAGUMO')], default=1),
        ),
    ]
