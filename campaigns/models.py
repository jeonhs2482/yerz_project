from django.db import models

class SubTitle(models.Model):
    brand = models.CharField(max_length=64)
    host  = models.CharField(max_length=64)

    class Meta:
        db_table = 'subtitles'

class Campaign(models.Model):
    image    = models.CharField(max_length=256)
    title    = models.CharField(max_length=64)
    subtitle = models.ForeignKey('SubTitle', on_delete=models.CASCADE)

    class Meta:
        db_table = 'campaigns'

class Option(models.Model):
    title    = models.CharField(max_length=64)
    price    = models.IntegerField()
    quantity = models.PositiveSmallIntegerField(default=0)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)

    class Meta:
        db_table = 'options'
