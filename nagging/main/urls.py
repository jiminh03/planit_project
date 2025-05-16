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
]
