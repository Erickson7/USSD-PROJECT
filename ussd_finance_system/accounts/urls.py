from django.urls import path
from .views import (
    register_trader,
    register_success,
    trader_login,
    trader_dashboard,
    trader_logout
)

urlpatterns = [
    path('register/', register_trader, name='register'),
    path('register-success/', register_success, name='register_success'),

    path('login/', trader_login, name='login'),
    path('dashboard/', trader_dashboard, name='dashboard'),
    path('logout/', trader_logout, name='logout'),
]