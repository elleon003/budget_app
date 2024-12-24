from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def transaction_list(request):
    """View to list all transactions."""
    return render(request, 'transactions/transaction_list.html', {
        'transactions': []  # Placeholder for transactions
    })
