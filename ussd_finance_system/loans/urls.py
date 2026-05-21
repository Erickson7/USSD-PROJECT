from django.urls import path
from .views import (
    request_loan,
    my_loans,
    repay_loan
)

urlpatterns = [
    path('request/', request_loan),
    path('my-loans/', my_loans),

    path(
        'repay/<int:loan_id>/',
        repay_loan,
        name='repay_loan'
    ),
]