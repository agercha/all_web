# Generated by Django 4.1.1 on 2022-11-10 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doodleio', '0002_playeritem_ingameroom_alter_playeritem_isdrawing'),
    ]

    operations = [
        migrations.AddField(
            model_name='playeritem',
            name='guessedRight',
            field=models.BooleanField(default=False),
        ),
    ]