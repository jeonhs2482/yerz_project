from django.db import models

class Campaign(models.Model):
    image    = models.CharField(max_length=256)
    title    = models.CharField(max_length=64)
    brand    = models.CharField(max_length=64)
    host     = models.CharField(max_length=64)
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_campaign')

    class Meta:
        db_table = 'campaigns'

class Option(models.Model):
    title    = models.CharField(max_length=64)
    price    = models.IntegerField()
    quantity = models.PositiveSmallIntegerField(default=0)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)

    class Meta:
        db_table = 'options'
