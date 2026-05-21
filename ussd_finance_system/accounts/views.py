from django.shortcuts import render, redirect
from .models import Trader
from django.http import HttpResponse


def register_trader(request):

    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        pin = request.POST.get('pin')

        Trader.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            pin=pin
        )

        return redirect('/accounts/register-success/')

    return render(request, 'accounts/register.html')
def register_success(request):
    return render(request, 'accounts/register_success.html')

def trader_login(request):

    if request.method == 'POST':

        phone_number = request.POST.get('phone_number')
        pin = request.POST.get('pin')

        try:
            trader = Trader.objects.get(
                phone_number=phone_number,
                pin=pin
            )

            request.session['trader_id'] = trader.id

            return redirect('/accounts/dashboard/')

        except Trader.DoesNotExist:

            return HttpResponse("Invalid Phone Number or PIN")

    return render(request, 'accounts/login.html')

def trader_dashboard(request):

    trader_id = request.session.get('trader_id')

    if not trader_id:
        return redirect('/accounts/login/')

    trader = Trader.objects.get(id=trader_id)

    return render(request, 'accounts/dashboard.html', {
        'trader': trader
    })

def trader_logout(request):

    request.session.flush()

    return redirect('/accounts/login/')
