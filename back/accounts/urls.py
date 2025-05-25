from django.urls import path
from .views import SignupView, LoginView, LogoutView, MeView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),  # 로그인 상태 확인 API
]