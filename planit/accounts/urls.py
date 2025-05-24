from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.login, name = 'login'),
    path('signup/', views.signup, name = 'signup'),
    path('signup/complete/', views.signup_complete, name='signup_complete'),
    path('function/', views.function, name = 'function'),
    path('notice/', views.notice, name = 'notice'),
    path('logout/', views.logout_view, name='logout'),
    path("google/callback/", views.google_callback, name="google_callback"),
    path('naver/callback/', views.naver_callback, name='naver_callback'),
    path('api/signup/', views.signup_api, name='signup_api'),
    path('api/login/', views.login_api, name='login_api'),
]
