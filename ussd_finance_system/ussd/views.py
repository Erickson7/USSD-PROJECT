from django.http import HttpResponse
from datetime import date, timedelta

from accounts.models import Trader
from transactions.models import Transaction
from loans.models import Loan, LoanRepayment
from transactions.models import Transaction, Debt
from tax.models import Tax, TaxPayment
from ussd_finance_system.sms import sms
from django.views.decorators.csrf import csrf_exempt



def send_sms(phone, message):

    try:

        sms.send(
            message,
            [phone]
        )

        print("SMS Sent Successfully")

    except Exception as e:

        print(e)


def calculate_loan_score(trader):

    score = 0

    # SALES SCORE
    sales = Transaction.objects.filter(
        trader=trader,
        transaction_type="SALE"
    )

    total_sales = sum(
        sale.amount for sale in sales
    )

    if total_sales >= 50000:
        score += 40

    elif total_sales >= 20000:
        score += 20

    # EXPENSE SCORE
    expenses = Transaction.objects.filter(
        trader=trader,
        transaction_type="EXPENSE"
    )

    total_expenses = sum(
        expense.amount for expense in expenses
    )

    if total_expenses < total_sales:
        score += 20

    # REPAYMENT HISTORY
    paid_loans = Loan.objects.filter(
        trader=trader,
        status="PAID"
    ).count()

    score += paid_loans * 10

    # OVERDUE PENALTY
    overdue_loans = Loan.objects.filter(
        trader=trader,
        status="OVERDUE"
    ).count()

    score -= overdue_loans * 50

    # PENALTY HISTORY
    penalty_loans = Loan.objects.filter(
        trader=trader,
        penalty_amount__gt=0
    ).count()

    score -= penalty_loans * 30

    return score




@csrf_exempt
def ussd_callback(request):


    text = request.POST.get('text', '')
    user_response = text.split('*')

    response = ""

    # =====================================
    # MAIN MENU
    # =====================================

    if text == "":

        response = "CON Welcome\n"
        response += "1. Register\n"
        response += "2. Login"


    # =====================================
    # REGISTER
    # =====================================

    elif text == "1":

        response = "CON Enter Full Name"

    elif len(user_response) == 2 and user_response[0] == "1":

        response = "CON Enter Business Name"

    elif len(user_response) == 3 and user_response[0] == "1":

        response = "CON Enter Phone Number"

    elif len(user_response) == 4 and user_response[0] == "1":

        response = "CON Enter National ID"

    elif len(user_response) == 5 and user_response[0] == "1":

        response = "CON Create PIN"

    elif len(user_response) == 6 and user_response[0] == "1":

        Trader.objects.create(

            full_name=user_response[1],

            business_name=user_response[2],

            phone_number=user_response[3],

            national_id=user_response[4],

            pin=user_response[5]
        )

        response = "END Registration Successful"

    # =====================================
    # LOGIN
    # =====================================

    elif text == "2":

        response = "CON Enter PIN"

    elif len(user_response) == 2 and user_response[0] == "2":

        pin = user_response[1]

        try:

            Trader.objects.get(pin=pin)

            response = "CON Choose Option\n"
            response += "1. Record Sale\n"
            response += "2. Record Expense\n"
            response += "3. Financial Summary\n"
            response += "4. Loans\n"
            response += "5. Income\n"
            response +="6. Tax\n"
            response += "7. Record Debts\n"
            response += "8. Logout"

        except Trader.DoesNotExist:

            response = "END Invalid PIN"

    # =====================================
    # MAIN MENU ACTIONS
    # =====================================

    elif len(user_response) == 3 and user_response[0] == "2":

        pin = user_response[1]

        try:

            trader = Trader.objects.get(pin=pin)

            option = user_response[2]

            # =====================================
            # RECORD SALE
            # =====================================

            if option == "1":

                response = "CON Enter Sale Amount"

            # =====================================
            # RECORD EXPENSE
            # =====================================

            elif option == "2":

                response = "CON Enter Expense Amount"

            # =====================================
            # FINANCIAL SUMMARY
            # =====================================

            elif option == "3":

                sales = Transaction.objects.filter(
                    trader=trader,
                    transaction_type="SALE"
                )

                expenses = Transaction.objects.filter(
                    trader=trader,
                    transaction_type="EXPENSE"
                )

                total_sales = sum(s.amount for s in sales)
                total_expenses = sum(e.amount for e in expenses)

                balance = total_sales - total_expenses

                response = (
                    f"END Sales: {total_sales}\n"
                    f"Expenses: {total_expenses}\n"
                    f"Balance: {balance}"
                )

            # =====================================
            # LOANS MENU
            # =====================================

            elif option == "4":

                response = "CON Loans Menu\n"
                response += "1. Request Loan\n"
                response += "2. View Loans\n"
                response += "3. Repay Loan"

            # =====================================
            # INCOME
            # =====================================

            elif option == "5":

                sales = Transaction.objects.filter(
                    trader=trader,
                    transaction_type="SALE"
                )

                total_income = sum(s.amount for s in sales)

                response = f"END Total Income: {total_income}"


                # =====================================
                # TAX MENU
                # =====================================

            elif option=="6":
                response="CON Tax Menu\n"
                response +="1.View Tax\n"
                response +="2.Pay Tax"

           # =====================================
           # RECORD DEBTS
           # =====================================
            elif option=="7":
                response="CON Enter Customer Name\n"
                
            # =====================================
            # LOGOUT
            # =====================================

            elif option == "8":

                response = "END Logged Out Successfully"

            else:

                response = "END Invalid Option"

        except Trader.DoesNotExist:

            response = "END Invalid PIN"

    # =====================================
    # SALES / EXPENSE / LOANS
    # =====================================

    elif len(user_response) == 4 and user_response[0] == "2":

        pin = user_response[1]

        try:

            trader = Trader.objects.get(pin=pin)

            option = user_response[2]

            # =====================================
            # SAVE SALE
            # =====================================

            if option == "1":

                Transaction.objects.create(
                    trader=trader,
                    transaction_type="SALE",
                    amount=float(user_response[3]),
                    description="USSD Sale"
                )

                response = "END Sale Recorded Successfully"

            # =====================================
            # SAVE EXPENSE
            # =====================================

            elif option == "2":

                Transaction.objects.create(
                    trader=trader,
                    transaction_type="EXPENSE",
                    amount=float(user_response[3]),
                    description="USSD Expense"
                )

                response = "END Expense Recorded Successfully"

            # =====================================
            # LOAN OPTIONS
            # =====================================

            elif option == "4":

                loan_option = user_response[3]

                # =====================================
                # REQUEST LOAN
                # =====================================

                if loan_option == "1":

                    response = "CON Enter Loan Amount"

                # =====================================
                # VIEW LOANS
                # =====================================

                elif loan_option == "2":

                    loans = Loan.objects.filter(
                        trader=trader
                    )

                    if not loans.exists():

                        response = "END No Loans Found"

                    else:

                        latest_loan = loans.last()

                        response = (
                            f"END Amount: {latest_loan.loan_amount}\n"
                            f"Balance: {latest_loan.remaining_balance}\n"
                            f"Status: {latest_loan.status}"
                        )

                # =====================================
                # REPAY LOAN
                # =====================================

                elif loan_option == "3":

                    loan = Loan.objects.filter(
                        trader=trader,
                        remaining_balance__gt=0,
                        status="APPROVED"
                    ).first()

                    if not loan:

                        response = "END No active approved loan found"

                    else:

                        today = date.today()

                        # =====================================
                        # AUTOMATIC OVERDUE PENALTY
                        # =====================================

                        if loan.due_date and today > loan.due_date:

                            penalty = loan.remaining_balance * 0.10

                            loan.remaining_balance += penalty
                            loan.status = "OVERDUE"
                            # ADD 5% PENALTY
                            penalty = loan.remaining_balance * 0.05
                            loan.penalty_amount += penalty
                            loan.remaining_balance += penalty
                            

                            loan.save()

                            send_sms(
                                      trader.phone_number,
                                     f"WARNING: Your loan is overdue. Penalty has been added."
                              )

                            response = (
                                f"CON OVERDUE LOAN\n"
                                f"Penalty Added: {penalty}\n"
                                f"New Balance: {loan.remaining_balance}\n"
                                f"Enter repayment amount"
                            )

                        else:

                            response = (
                                f"CON Balance: {loan.remaining_balance}\n"
                                f"Enter repayment amount"
                            )

                else:

                    response = "END Invalid Loan Option"

            else:

                response = "END Invalid Option"

        except Trader.DoesNotExist:

            response = "END Invalid PIN"

    # =====================================
    # TAX OPTIONS
    # =====================================
    elif option=="6":
        tax_option=user_response[3]

        # VIEW TAX
        if tax_option=="1":
            sales=Transaction.objects.filter(
                trader=trader,
                transaction_type="SALE"
            )
            total_sales=sum(sale.amount for sale in sales)
            tax_amount=total_sales*0.05
            response=(
                f"END Total Sales:{total_sales}\n"
                f"Tax Due:{tax_amount}"
            )
            # PAY TAX
        elif tax_option=="2":
            response="CON Enter Tax Payment Amount"

        # =====================================
        # RECORD DEBT STEP1
        # =====================================
        elif option == "7":
            response="CON Enter Debt Amount\n"
            
    # =====================================
    # FINAL STEP
    # =====================================

    elif len(user_response) == 5 and user_response[0] == "2":

        pin = user_response[1]

        try:

            trader = Trader.objects.get(pin=pin)

            # =====================================
            # REQUEST LOAN FINAL
            # =====================================

            if user_response[2] == "4" and user_response[3] == "1":

                amount = float(user_response[4])

                # =====================================
                # CALCULATE SCORE
                # =====================================

                score = calculate_loan_score(
                    trader
                )

                # =====================================
                # AUTO APPROVE / REJECT
                # =====================================

                if score >= 60:

                    loan_status = "APPROVED"

                else:

                    loan_status = "REJECTED"

                Loan.objects.create(

                    trader=trader,

                    loan_amount=amount,

                    total_amount=amount,

                    remaining_balance=amount,

                    duration_months=6,

                    interest_rate=10,

                    due_date=date.today() + timedelta(days=30 * 6),

                    status=loan_status,

                    credit_score=score,

                )

                # =====================================
                # FINAL RESPONSE
                # =====================================

                if loan_status == "APPROVED":

                    send_sms(
                        trader.phone_number,
                      f"Hello {trader.full_name}, your loan of {amount} has been APPROVED."
                   )


                    response = (
                        f"END Loan Approved\n"
                        f"Credit Score: {score}"
                    )

                else:

                    send_sms(
                          trader.phone_number,
                         f"Hello {trader.full_name}, your loan request has been REJECTED."
                     )

                    response = (
                        f"END Loan Rejected\n"
                        f"Credit Score: {score}"
                    )

            # =====================================
            # REPAYMENT FINAL
            # =====================================

            elif user_response[2] == "4" and user_response[3] == "3":

                repay_amount = float(user_response[4])

                loan = Loan.objects.filter(
                    trader=trader,
                    remaining_balance__gt=0
                ).first()

                if not loan:

                    response = "END No active loan found"

                else:

                    if repay_amount > loan.remaining_balance:

                        response = "END Amount exceeds remaining balance"

                    else:

                        # SAVE REPAYMENT HISTORY
                        LoanRepayment.objects.create(
                            loan=loan,
                            amount_paid=repay_amount
                        )

                        # UPDATE BALANCE
                        loan.remaining_balance -= repay_amount

                        # FULL PAYMENT
                        if loan.remaining_balance <= 0:

                            loan.remaining_balance = 0
                            loan.status = "PAID"

                        else:

                            if loan.due_date and loan.due_date < date.today():

                                loan.status = "OVERDUE"

                        loan.save()

                        send_sms(
                                 trader.phone_number,
                             f"Payment received. Remaining balance is {loan.remaining_balance}"
                      )

                        response = (
                            f"END Payment Successful\n"
                            f"Remaining Balance: {loan.remaining_balance}"
                        )

            # =====================================
            # TAX PAYMENT
            # =====================================
            elif user_response[2] == "6" and user_response[3] == "2":

                payment_amount = float(user_response[4])

                receipt = f"TXN-{trader.id}-{date.today()}"

                TaxPayment.objects.create(
                    trader=trader,
                    amount_paid=payment_amount,
                    receipt_number=receipt
                )

                response = (
                    f"END Tax Payment Successful\n"
                    f"Receipt: {receipt}"
                )

            # =====================================
            # SAVE DEBT
            # =====================================
            elif user_response[2] == "7":
                customer_name = user_response[3]
                amount = float(user_response[4])
                Debt.objects.create(
                    trader=trader,
                    customer_name=customer_name,
                    amount=amount
                )
                response = (
                    f"END Debt Recorded Successfully\n"
                    f"Customer: {customer_name}\n"
                    f"Amount: {amount}"
                )

            else:

                response = "END Invalid Request"

        except Trader.DoesNotExist:

            response = "END Invalid PIN"


    






    # =====================================
    # DEFAULT ERROR
    # =====================================

    else:

        response = "END Invalid Request"

    return HttpResponse(response)