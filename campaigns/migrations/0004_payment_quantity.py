# Generated by Django 3.2.4 on 2021-06-16 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0003_auto_20210616_0642'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
