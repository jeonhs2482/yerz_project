from django.db import models

class User(models.Model):
    email        = models.CharField(max_length=64)
    password     = models.CharField(max_length=64)
    name         = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    user_option  = models.ManyToManyField('campaigns.Option', through='UserOption')
    payment      = models.ManyToManyField('campaigns.Campaign', through='Payment')

    class Meta:
        db_table = 'users'

class UserOption(models.Model):
    title    = models.CharField(max_length=128)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()
    user     = models.ForeignKey('User', on_delete=models.CASCADE, related_name='useroption')
    option   = models.ForeignKey('campaigns.Option', on_delete=models.CASCADE, related_name='useroption')
    
    class Meta:
        db_table = 'user_option'

class Payment(models.Model):
    name             = models.CharField(max_length=64)
    phone_number     = models.CharField(max_length=64)
    address          = models.CharField(max_length=128)
    delivery_request = models.CharField(max_length=128)
    payment_type     = models.CharField(max_length=64, default='')
    created_at       = models.DateTimeField(auto_now_add=True)
    user             = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_payment')
    campaign         = models.ForeignKey('campaigns.Campaign', on_delete=models.CASCADE, related_name='campaign_payment')
    
    class Meta:
        db_table = 'payments'