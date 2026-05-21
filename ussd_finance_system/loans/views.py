from django.shortcuts import render, redirect
from .models import Loan
from accounts.models import Trader
from datetime import date, timedelta
from .models import Loan, LoanRepayment 


def request_loan(request):

    trader_id = request.session.get('trader_id')

    if not trader_id:
        return redirect('/accounts/login/')

    trader = Trader.objects.get(id=trader_id)

    if request.method == 'POST':

        loan_amount = float(
            request.POST.get('loan_amount')
        )

        interest_rate = float(
            request.POST.get('interest_rate')
        )

        duration_months = int(
            request.POST.get('duration_months')
        )

        purpose = request.POST.get('purpose')

        interest = (
            loan_amount * interest_rate / 100
        )

        total_amount = loan_amount + interest

        remaining_balance = total_amount

        due_date = date.today() + timedelta(
            days=30 * duration_months
        )

        Loan.objects.create(
            trader=trader,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            total_amount=total_amount,
            remaining_balance=remaining_balance,
            duration_months=duration_months,
            purpose=purpose,
            due_date=due_date
        )

        return redirect('/loans/my-loans/')

    return render(
        request,
        'loans/request_loan.html'
    )


def my_loans(request):

    trader_id = request.session.get('trader_id')

    if not trader_id:
        return redirect('/accounts/login/')

    loans = Loan.objects.filter(
        trader_id=trader_id
    )

    return render(
        request,
        'loans/my_loans.html',
        {'loans': loans}
    )

def repay_loan(request, loan_id):

    trader_id = request.session.get('trader_id')

    if not trader_id:
        return redirect('/accounts/login/')

    loan = Loan.objects.get(id=loan_id)

    if request.method == 'POST':

        payment = float(
            request.POST.get('amount_paid')
        )

        LoanRepayment.objects.create(
            loan=loan,
            amount_paid=payment
        )

        loan.amount_paid += payment

        loan.remaining_balance -= payment

        if loan.remaining_balance <= 0:
            loan.status = 'COMPLETED'
            loan.remaining_balance = 0

        loan.save()

        return redirect('/loans/my-loans/')

    return render(
        request,
        'loans/repay_loan.html',
        {'loan': loan}
    )
