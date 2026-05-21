from django.contrib import admin
from .models import Loan, LoanRepayment


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):

    list_display = (
        'trader',
        'loan_amount',
        'remaining_balance',
        'status',
        'due_date'
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'trader__full_name',
    )


@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):

    list_display = (
        'loan',
        'amount_paid',
        'payment_date'
    )
