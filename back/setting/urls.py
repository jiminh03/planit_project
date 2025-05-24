from .views import MonthlyBudgetView, FixedExpenseView, PredictedFixedExpensesView, PasswordChangeView, download_expense_data, AccountDeleteView
from django.urls import path

urlpatterns = [
    path('budget/', MonthlyBudgetView.as_view(), name='monthly-budget'),
    path('fixed-expenses/', FixedExpenseView.as_view(), name='fixed-expenses'),
    path('predicted-expenses/', PredictedFixedExpensesView.as_view(), name='predicted-expenses'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('download/expense-data/', download_expense_data, name='download-expense-data'),
    path('accounts/delete/', AccountDeleteView.as_view(), name='account-delete'),
]