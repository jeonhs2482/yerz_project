# Generated by Django 3.2.4 on 2021-06-11 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_campaign_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='user',
        ),
    ]