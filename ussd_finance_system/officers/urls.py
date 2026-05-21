from django.urls import path

from .views import (
    officer_login,
    officer_dashboard,
    officer_logout,
    approve_loan,
    reject_loan,
    traders_list,
)

urlpatterns = [
    path('', officer_login, name='officer_login'),
    path('dashboard/', officer_dashboard, name='officer_dashboard'),
    path('logout/', officer_logout, name='officer_logout'),
    path('approve-loan/<int:loan_id>/', approve_loan, name='approve_loan'),
    path('reject-loan/<int:loan_id>/', reject_loan, name='reject_loan'),
    path('traders/', traders_list, name='traders_list'),
]