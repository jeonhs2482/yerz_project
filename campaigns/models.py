from django.db import models
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
class Option(models.Model):
    title    = models.CharField(max_length=64)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=0)
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    payment  = models.ForeignKey('Payment', on_delete=models.CASCADE, default='')
    class Meta:
        db_table = 'options'
class Payment(models.Model):
    payment_type     = models.CharField(max_length=64)
    name             = models.CharField(max_length=64, default='')
    phone_number     = models.CharField(max_length=64, default='')
    address          = models.CharField(max_length=128, default='')
    delivery_request = models.CharField(max_length=128, default='')
    created_at       = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'payments'