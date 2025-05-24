from django.urls import path
from .views import SpendingReportView

urlpatterns = [
    path('summary/', SpendingReportView.as_view(), name='spending-summary'),
]
