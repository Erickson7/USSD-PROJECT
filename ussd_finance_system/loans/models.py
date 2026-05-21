from datetime import date
from django.db import models
from accounts.models import Trader



class Loan(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    )

    trader = models.ForeignKey(
        Trader,
        on_delete=models.CASCADE
    )

    loan_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    remaining_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10
    )

    penalty_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    duration_months = models.IntegerField(
        default=6
    )

    application_date = models.DateField(
        default=date.today
    )

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    rejection_reason = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    credit_score = models.IntegerField(
    default=0
)


    def __str__(self):
        return f"{self.trader.full_name} - {self.loan_amount}"


class LoanRepayment(models.Model):

    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_date = models.DateField(
        default=date.today
    )

    def __str__(self):
        return f"{self.loan.trader.full_name} - {self.amount_paid}"


