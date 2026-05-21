from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from loans.models import Loan, LoanRepayment
from accounts.models import Trader
from tax.models import Tax, TaxPayment
from transactions.models import Transaction
from loans.scoring import calculate_loan_score
from datetime import date


def officer_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('officer_dashboard')

    return render(
        request,
        'officers/login.html'
    )



def officer_dashboard(request):

    pending_loans = Loan.objects.filter(
        status="PENDING"
    )
    approved_loans = Loan.objects.filter(
        status="APPROVED"
    )

    overdue_loans = Loan.objects.filter(
        status="OVERDUE"
    )
    repayments = LoanRepayment.objects.all().order_by('-payment_date')

    traders = Trader.objects.all()
    monthly_tax = TaxPayment.objects.all()

    # =====================================
    # FINANCIAL ANALYTICS
    # =====================================

    total_sales = sum(
        t.amount for t in Transaction.objects.filter(
            transaction_type="SALE"
        )
    )

    total_expenses = sum(
        t.amount for t in Transaction.objects.filter(
            transaction_type="EXPENSE"
        )
    )

    total_income = total_sales - total_expenses

    total_loans = sum(
        loan.loan_amount for loan in approved_loans
    )

    total_penalties = sum(
        loan.penalty_amount for loan in overdue_loans
    )
    taxes = Tax.objects.all()

    today = date.today()

    for tax in taxes:
        if (
            tax.due_date and
            tax.due_date < today and
            tax.status != "PAID"
        ):
         if tax.penalty_amount == 0:
            penalty = tax.tax_amount * 0.05
            tax.penalty_amount = penalty
            tax.status = "OVERDUE"
            tax.save()

    context = {
        'pending_loans': pending_loans,
        'approved_loans': approved_loans,
        'overdue_loans': overdue_loans,
        'repayments': repayments,
        'traders': traders,
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'total_income': total_income,
        'total_loans': total_loans,
        'total_penalties': total_penalties,
        'taxes': taxes,
        'monthly_tax': monthly_tax,
    }

    return render(
        request,
        'officers/dashboard.html',
        context
    )

def approve_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    loan.status = "APPROVED"
    loan.save()

    return redirect('officers:loan_list')  # adjust to your URL name

def reject_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    loan.status = "REJECTED"
    loan.save()

    return redirect('officers:loan_list')  # adjust if needed


def traders_list(request):

    traders = Trader.objects.all()

    context = {
        'traders': traders
    }

    return render(
        request,
        'officers/traders_list.html',
        context
    )


def officer_logout(request):

    logout(request)

    return redirect('officer_login')
