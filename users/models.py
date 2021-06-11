from django.db import models
class User(models.Model):
    email     = models.CharField(max_length=64)
    password  = models.CharField(max_length=64, blank=False)
    campaigns = models.ManyToManyField('campaigns.Campaign', through='UserCampaign', related_name='users')
    class Meta:
        db_table = 'users'
class UserCampaign(models.Model):
    user     = models.ForeignKey('User', on_delete=models.CASCADE)
    campaign = models.ForeignKey('campaigns.Campaign', on_delete=models.CASCADE)
    class Meta:
        db_table = 'user_campaign'