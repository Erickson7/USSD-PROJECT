from django.db import models

class Trader(models.Model):
    full_name = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    national_id = models.CharField(max_length=30)
    pin = models.CharField(max_length=10)

    def __str__(self):
        return self.full_name
