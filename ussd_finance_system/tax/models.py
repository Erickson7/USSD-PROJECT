from django.db import models
from accounts.models import Trader


class Tax(models.Model):

    trader = models.ForeignKey(
        Trader,
        on_delete=models.CASCADE
    )

    total_sales = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5
    )

    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    penalty_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default="PENDING"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.trader.full_name} - Tax"


class TaxPayment(models.Model):

    trader = models.ForeignKey(
        Trader,
        on_delete=models.CASCADE
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    receipt_number = models.CharField(
        max_length=100,
        unique=True
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        default="PAID"
    )

    def __str__(self):

        return f"{self.trader.full_name} - {self.amount_paid}"
