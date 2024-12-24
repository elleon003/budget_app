from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def account_list(request):
    """View to list all bank accounts."""
    return render(request, 'banking/account_list.html', {
        'accounts': []  # Placeholder for bank accounts
    })
