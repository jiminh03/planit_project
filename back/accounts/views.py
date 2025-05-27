from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import SignupSerializer
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.pagination import PageNumberPagination
from .models import Notice
from .serializers import NoticeSerializer
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.exceptions import PermissionDenied
import os
from urllib.parse import urlencode
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from rest_framework.generics import ListAPIView

User = get_user_model()

# 회원가입
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 완료'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': '이메일과 비밀번호를 모두 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return Response({'message': '로그인 성공', 'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'isAdmin': user.is_staff
            }})
        else:
            return Response({'error': '이메일 또는 비밀번호가 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

# 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth_logout(request)  # 서버 세션 비우기
        request.session.flush()  # 세션 데이터 완전 삭제
        response = Response({'message': '로그아웃 되었습니다.'}, status=status.HTTP_200_OK)
        # 클라이언트 쿠키 삭제
        response.delete_cookie('sessionid', path='/')
        response.delete_cookie('csrftoken', path='/')
        # 추가: 캐시 무효화 헤더 추가
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

# 로그인 상태 확인
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'is_staff': user.is_staff  # ✅ 관리자 여부 포함
        })
    
class NoticePagination(PageNumberPagination):
    page_size = 10
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data,
        })

# 공지사항 조회


class NoticeListView(ListAPIView):
    queryset = Notice.objects.all().order_by('-created_at', '-updated_at')
    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]
    pagination_class = NoticePagination  # 👈 page_size=5 적용됨


# 공지사항 목록 자세히 보기
class NoticeDetailView(RetrieveAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [AllowAny]  # ✅ 이 줄 추가

# # 공지사항 생성 (관리자만)
# from rest_framework.permissions import IsAuthenticated
# class NoticeCreateAPIView(CreateAPIView):
#     queryset = Notice.objects.all()
#     serializer_class = NoticeSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         if not self.request.user.is_staff:
#             raise PermissionDenied("관리자만 공지사항을 작성할 수 있습니다.")
#         serializer.save()

# 구글 로그인
@method_decorator(csrf_exempt, name='dispatch')
class GoogleLoginURLView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # ✅ 인증도 비활성화

    def get(self, request):
        redirect_uri = 'http://localhost:8000/api/accounts/google/callback/'
        print('🔍 Google OAuth redirect_uri:', redirect_uri)  # 디버깅용 로그
        query = urlencode({
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'prompt': 'select_account'
        })
        return Response({'auth_url': f'https://accounts.google.com/o/oauth2/v2/auth?{query}'})
    
@method_decorator(csrf_exempt, name='dispatch')
class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # ✅ 인증 비활성화

    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return Response({'error': 'No code'}, status=400)

        token_res = requests.post('https://oauth2.googleapis.com/token', data={
            'code': code,
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'redirect_uri': 'http://localhost:8000/api/accounts/google/callback/',
            'grant_type': 'authorization_code'
        }).json()

        access_token = token_res.get('access_token')
        userinfo = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        ).json()

        email = userinfo.get('email')
        name = userinfo.get('name')

        user, _ = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name': name})
        auth_login(request, user)
        return redirect('http://localhost:5173/home')  # ✅ Vue 앱 홈으로 이동
    
    
@method_decorator(csrf_exempt, name='dispatch')
class NaverLoginURLView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        client_id = os.getenv("NAVER_CLIENT_ID")
        redirect_uri = "http://localhost:8000/api/accounts/naver/callback/"
        state = get_random_string(12)
        query = urlencode({
            'response_type': 'code',
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'state': state,
        })
        return JsonResponse({
            'auth_url': f"https://nid.naver.com/oauth2.0/authorize?{query}"
        })

@method_decorator(csrf_exempt, name='dispatch')
class NaverCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        code = request.GET.get("code")
        state = request.GET.get("state")

        token_url = "https://nid.naver.com/oauth2.0/token"
        token_params = {
            'grant_type': 'authorization_code',
            'client_id': os.getenv("NAVER_CLIENT_ID"),
            'client_secret': os.getenv("NAVER_CLIENT_SECRET"),
            'code': code,
            'state': state,
        }
        token_res = requests.get(token_url, params=token_params).json()
        access_token = token_res.get("access_token")

        profile_url = "https://openapi.naver.com/v1/nid/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_res = requests.get(profile_url, headers=headers).json()
        naver_info = profile_res.get("response")

        if not naver_info:
            return redirect("http://localhost:5173/login")

        email = naver_info.get("email")
        name = naver_info.get("name") or naver_info.get("nickname")
        if not name:
            name = f"네이버사용자_{get_random_string(6)}"

        user, _ = User.objects.get_or_create(
            username=email,
            defaults={'email': email, 'first_name': name}
        )

        auth_login(request, user)
        return redirect("http://localhost:5173/home")