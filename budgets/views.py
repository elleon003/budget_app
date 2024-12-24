from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def budget_list(request):
    """View to list all budgets."""
    return render(request, 'budgets/budget_list.html', {
        'budgets': []  # Placeholder for budgets
    })
