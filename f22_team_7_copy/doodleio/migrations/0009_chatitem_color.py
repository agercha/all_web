# Generated by Django 4.1.1 on 2022-12-01 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doodleio', '0008_playeritem_inleaderboardroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatitem',
            name='color',
            field=models.CharField(default=2, max_length=20),
            preserve_default=False,
        ),
    ]
