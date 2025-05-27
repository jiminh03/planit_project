from django.urls import path
from .views import SpendingHelperView

urlpatterns = [
    path('analysis/', SpendingHelperView.as_view(), name='spending-helper'),
]
