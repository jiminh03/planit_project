from django.urls import path
from .views import SpendingHelperView

urlpatterns = [
    path('helper/', SpendingHelperView.as_view(), name='spending-helper'),
]
