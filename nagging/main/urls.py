from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'), 
    path('report/', views.report, name='report'),
    path('helper/', views.helper, name='helper'),
    path('settings/', views.settings, name='settings'),
]
