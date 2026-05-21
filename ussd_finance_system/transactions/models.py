from django.db import models
from accounts.models import Trader

class Transaction(models.Model):

    TRANSACTION_TYPES = (
        ('SALE', 'Sale'),
        ('EXPENSE', 'Expense'),
    )

    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trader.full_name} - {self.transaction_type}"


    
class Debt(models.Model):
    trader=models.ForeignKey(Trader,on_delete=models.CASCADE)
    customer_name=models.CharField(max_length=100)
    amount=models.DecimalField(max_digits=12, decimal_places=2)
    status=models.CharField(max_length=20,default="UNPAID")
    created_at=models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.customer_name}-{self.amount}"

