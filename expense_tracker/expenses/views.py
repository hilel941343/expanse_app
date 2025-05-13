from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from datetime import date
from django.db.models import Sum
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'expenses/register.html', {'form': form})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('summary')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})


from django.shortcuts import render
from django.db.models import Sum
from datetime import date
from .models import Expense  # Assuming you're using an Expense model


@login_required
def summary(request):
    today = date.today()
    this_month = today.month
    this_year = today.year

    expenses = Expense.objects.filter(user=request.user)

    # Daily Expenses
    daily_expenses = expenses.filter(date=today)
    daily_total = daily_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    daily_by_category = daily_expenses.values('category').annotate(total=Sum('amount'))

    # Monthly Expenses
    monthly_expenses = expenses.filter(date__month=this_month, date__year=this_year)
    monthly_total = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_by_category = monthly_expenses.values('category').annotate(total=Sum('amount'))

    # Yearly Expenses
    yearly_expenses = expenses.filter(date__year=this_year)
    yearly_total = yearly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    yearly_by_category = yearly_expenses.values('category').annotate(total=Sum('amount'))

    # Passing data to the template as a list of dictionaries
    summaries = [
        {
            'period': 'Today',
            'total': daily_total,
            'breakdown': daily_by_category,
        },
        {
            'period': 'This Month',
            'total': monthly_total,
            'breakdown': monthly_by_category,
        },
        {
            'period': 'This Year',
            'total': yearly_total,
            'breakdown': yearly_by_category,
        },
    ]

    context = {
        'summaries': summaries,
    }

    return render(request, 'summary.html', context)


@login_required
def my_expenses(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'my_expenses.html', {'expenses': expenses})
