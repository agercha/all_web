# Generated by Django 4.1.1 on 2022-11-10 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doodleio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playeritem',
            name='inGameRoom',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='playeritem',
            name='isDrawing',
            field=models.BooleanField(default=False),
        ),
    ]
