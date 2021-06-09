from django.db import models

class User(models.Model):
    email    = models.CharField(max_length=64)
    password = models.CharField(max_length=64, blank=False)
    campaign = models.ManyToManyField('Campaign', through='UserCampaign', related_name='users')

    class Meta:
        db_table = 'users'