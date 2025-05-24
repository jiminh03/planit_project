from django.urls import path
from django.contrib.auth.views import PasswordChangeView
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'), 
    path('report/', views.report, name='report'),
    path('helper/', views.helper, name='helper'),
    path('setting/', views.setting, name='setting'),
    path('delete/', views.delete_account, name='delete'),
    path('password/', PasswordChangeView.as_view(
        template_name='main/password_change.html',
        success_url='/main/setting/'), name='password_change'), 
    path('create_expense/', views.create_expense, name='create_expense'),
    path('create_income/', views.create_income, name='create_income'),
    path('expense/<int:pk>/edit/', views.update_expense, name='update_expense'),
    path('expense/<int:pk>/delete/', views.delete_expense, name='delete_expense'),
    path('download/', views.download_expense_data, name='download'),
    path('fixed-expense/', views.fixed_expense_input, name='fixed_expense_input'),
    path('monthly-budget/', views.monthly_budget_view, name='monthly_budget'),
    path('delete/', views.delete_account, name='delete_confirm'),
    path('calendar-data/', views.calendar_data, name='calendar_data'),
]
