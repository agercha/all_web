# Generated by Django 4.1.1 on 2022-10-03 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0014_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pfp_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]