from django.urls import path
from .views import (
    SignupView, LoginView, LogoutView, MeView,
    NoticeListView, NoticeDetailView, NoticeCreateAPIView,
    GoogleCallbackView, GoogleLoginURLView, NaverLoginURLView, NaverCallbackView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),  # 로그인 상태 확인 API
    path('notice/', NoticeListView.as_view(), name='notice-list'),
    path('notice/<int:pk>/', NoticeDetailView.as_view()),  # ✅ 상세 보기 경로
    path('notice/create/', NoticeCreateAPIView.as_view(), name='notice-create'),
    path('google/login-url/', GoogleLoginURLView.as_view()),
    path('google/callback/', GoogleCallbackView.as_view()),
    path('naver/login-url/', NaverLoginURLView.as_view()),
    path('naver/callback/', NaverCallbackView.as_view()),
]