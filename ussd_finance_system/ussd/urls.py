from django.urls import path

from ussd_finance_system.accounts import views
from .views import ussd_callback

urlpatterns = [
    path("callback/",views.ussd_callback, name="ussd_callback"),
]