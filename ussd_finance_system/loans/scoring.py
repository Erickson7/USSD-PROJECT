
def calculate_loan_score(user):
    score = 0

    if user.has_active_loans:
        score += 20

    if user.has_good_repayment_history:
        score += 50

    return score