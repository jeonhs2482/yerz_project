from django.db import models
from django.db.models.deletion import SET_DEFAULT

class User(models.Model):
    email        = models.CharField(max_length=64)
    kakao_email  = models.CharField(max_length=64, default='')
    password     = models.CharField(max_length=64)
    name         = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    admin        = models.PositiveIntegerField(default=0)
    payment      = models.ManyToManyField('campaigns.Option', through='Payment')

    class Meta:
        db_table = 'users'

class PaymentOption(models.Model):
    title    = models.CharField(max_length=128)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()
    payment  = models.ForeignKey('Payment', on_delete=models.CASCADE, related_name='payment_option')
    
    class Meta:
        db_table = 'payment_option'

class Payment(models.Model):
    orderer_name     = models.CharField(max_length=64, default='')
    orderer_contact  = models.CharField(max_length=64, default='')
    name             = models.CharField(max_length=64)
    phone_number     = models.CharField(max_length=64)
    address          = models.CharField(max_length=128)
    delivery_request = models.CharField(max_length=128)
    payment_type     = models.CharField(max_length=64, default='')
    total            = models.IntegerField(default=0)
    created_at       = models.DateTimeField(auto_now_add=True)
    user             = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_payment')
    option           = models.ForeignKey('campaigns.Option', on_delete=models.CASCADE, related_name='option_payment', default=True)
    
    class Meta:
        db_table = 'payments'