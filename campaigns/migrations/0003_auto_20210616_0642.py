# Generated by Django 3.2.4 on 2021-06-16 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.DeleteModel(
            name='PaymentType',
        ),
    ]