# finance/urls.py
from django.urls import path
from .views import (
    CategoryListView,
    IncomeListView,
    ExpenseListView,
    BudgetListView,
    BudgetSummaryView,
    LoginView,
    TransactionListView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('incomes/', IncomeListView.as_view(), name='income-list'),
    path('expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('budgets/', BudgetListView.as_view(), name='budget-list'),
    path('budget-summary/', BudgetSummaryView.as_view(), name='budget-summary'),
    path('login/', LoginView.as_view(), name='login'), 
    path('transactions/', TransactionListView.as_view(), name='transactions'),
]
