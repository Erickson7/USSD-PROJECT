from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Transaction
from accounts.models import Trader
from django.db.models import Sum


def add_sale(request):

    if request.method == 'POST':

        trader_id = request.POST.get('trader')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        trader = Trader.objects.get(id=trader_id)

        Transaction.objects.create(
            trader=trader,
            transaction_type='SALE',
            amount=amount,
            description=description
        )

        return HttpResponse("Sale Recorded Successfully")

    traders = Trader.objects.all()

    return render(request, 'transactions/add_sale.html', {
        'traders': traders
    })


def add_expense(request):

    if request.method == 'POST':

        trader_id = request.POST.get('trader')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        trader = Trader.objects.get(id=trader_id)

        Transaction.objects.create(
            trader=trader,
            transaction_type='EXPENSE',
            amount=amount,
            description=description
        )

        return HttpResponse("Expense Recorded Successfully")

    traders = Trader.objects.all()

    return render(request, 'transactions/add_expense.html', {
        'traders': traders
    })
def financial_summary(request):

    sales = Transaction.objects.filter(
        transaction_type='SALE'
    ).aggregate(Sum('amount'))

    expenses = Transaction.objects.filter(
        transaction_type='EXPENSE'
    ).aggregate(Sum('amount'))

    total_sales = sales['amount__sum'] or 0
    total_expenses = expenses['amount__sum'] or 0

    profit = total_sales - total_expenses

    context = {
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'profit': profit
    }

    return render(
        request,
        'transactions/summary.html',
        context
    )
