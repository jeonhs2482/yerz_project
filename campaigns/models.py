from django.db import models

class Title(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'titles'

class SubTitle(models.Model):
    brand = models.CharField(max_length=64)
    host  = models.CharField(max_length=64)
    class Meta:
        db_table = 'subtitles'

class Campaign(models.Model):
    image    = models.CharField(max_length=128)
    title    = models.CharField(max_length=64)
    subtitle = models.ForeignKey('SubTitle', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'campaigns'

class UserCampaign(models.Model):
    user     = models.ForeignKey('User', on_delete=models.CASCADE)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_campaign'

class Option(models.Model):
    title    = models.CharField(max_length=64)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)

    class Meta:
        db_table = 'options'

class Payment(models.Model):
    payment_type = models.CharField(max_length=64)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'

class DeliveryInformation(models.Model):
    phone_number     = models.CharField(max_length=64)
    address          = models.CharField(max_length=128)
    delivery_request = models.CharField(max_length=128)
    option           = models.ForeignKey('Option', on_delete=models.CASCADE)

    class Meta:
        db_table = 'delivery_information'