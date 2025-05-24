from .views import MonthlyBudgetView, FixedExpenseView, PredictedFixedExpensesView, PasswordChangeView
from django.urls import path

urlpatterns = [
    path('budget/', MonthlyBudgetView.as_view(), name='monthly-budget'),
    path('fixed-expenses/', FixedExpenseView.as_view(), name='fixed-expenses'),
    path('predicted-expenses/', PredictedFixedExpensesView.as_view(), name='predicted-expenses'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
]