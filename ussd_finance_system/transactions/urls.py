from django.urls import path
from .views import (
    add_sale,
    add_expense,
    financial_summary
)

urlpatterns = [
    path('sale/', add_sale, name='add_sale'),
    path('expense/', add_expense, name='add_expense'),
    path('summary/', financial_summary, name='summary'),
]