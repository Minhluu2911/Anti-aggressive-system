# Generated by Django 4.0.3 on 2022-04-26 12:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmotionStat',
            new_name='EmotionData',
        ),
    ]