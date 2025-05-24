from django.urls import path
from .views import (
    IncomeListCreateView,
    ExpenseListCreateView,
    TransactionByDateView,
    IncomeDetailView,
    ExpenseDetailView,
    MonthlySummaryView,
    MonthlySummaryStatsView,
    TodaySummaryView,
    AIFeedbackView,
)

urlpatterns = [
    path('incomes/', IncomeListCreateView.as_view(), name='income-list-create'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('transactions/', TransactionByDateView.as_view(), name='transactions-by-date'),
    path('incomes/<int:pk>/', IncomeDetailView.as_view(), name='income-detail'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('monthly-summary/', MonthlySummaryView.as_view(), name='monthly-summary'),
    path('monthly-summary-stats/', MonthlySummaryStatsView.as_view(), name='monthly-summary-stats'),
    path('today-summary/', TodaySummaryView.as_view(), name='today-summary'),
    path('ai-feedback/', AIFeedbackView.as_view(), name='ai-feedback'),
]