from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, login as auth_login
from .forms import CustomUserCreationForm
from django.contrib.auth import logout as auth_logout
from .models import Notice
from django.core.paginator import Paginator
import os, requests
from django.conf import settings
import uuid
from django.utils.crypto import get_random_string


def index(request):
    return render(request, 'accounts/index.html')

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('main:home')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
        'NAVER_CLIENT_ID': settings.NAVER_CLIENT_ID,  # ✅ 추가
        'NAVER_CALLBACK_URI': settings.NAVER_CALLBACK_URI,  # ✅ 추가
        'STATE': uuid.uuid4().hex,  # ✅ 추가
    }
    return render(request, 'accounts/login.html', context)


# Vue 프론트에서 사용할 수 있는 JSON API 형태의 회원가입/로그인 API 추가
@csrf_exempt
def signup_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({"error": "JSON 형식이 올바르지 않습니다."}, status=400)

        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if not username or not password or not email:
            return JsonResponse({"error": "모든 항목을 입력해주세요."}, status=400)

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "이미 존재하는 사용자입니다."}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "이미 등록된 이메일입니다."}, status=400)

        User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({"message": "회원가입 성공"}, status=201)


@csrf_exempt
def login_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({"error": "JSON 형식이 올바르지 않습니다."}, status=400)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({"message": "로그인 성공"})
        else:
            return JsonResponse({"error": "로그인 실패"}, status=401)

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # 자동 로그인 없이 저장만
            return redirect('accounts:signup_complete')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/signup.html', context)

def signup_complete(request):
    return render(request, 'accounts/signup_complete.html')


def function(request):
    return render(request, 'accounts/function.html')

def notice(request):
    notices = Notice.objects.all().order_by('-created_at')
    paginator = Paginator(notices, 5)  # 5개씩 끊기
    page_number = request.GET.get('page')  # 현재 페이지 번호 받아오기
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'accounts/notice.html', context)

def logout_view(request):
    auth_logout(request)
    return redirect('accounts:index')  # 로그아웃 후 로그인 페이지로 이동


def get_access_token(code):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": "http://127.0.0.1:8000/accounts/google/callback/",
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()
    access_token = token_data.get("access_token")
    return access_token

def get_user_info(access_token):
    userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    userinfo_response = requests.get(
        userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    userinfo = userinfo_response.json()

    email = userinfo.get("email")
    name = userinfo.get("name")
    if not email or not name:
        return None, None
    return email, name


def google_callback(request):
    User = get_user_model()
    code = request.GET.get("code")
    if not code:
        print("No code provided")
        return redirect("/")

    access_token = get_access_token(code)
    email, name = get_user_info(access_token)

    if not email:
        print("User info not found")
        return redirect("/")

    # ✅ 기준은 email로, username은 랜덤
    user = User.objects.filter(email=email).first()

    if not user:
        user = User.objects.create(
            email=email,
            username=name,
            first_name=name,
        )
        print(f"User created: {user}")
    else:
        print(f"User exists: {user}")

    auth_login(request, user)
    return redirect("main:home")


def naver_callback(request):
    User = get_user_model()
    code = request.GET.get("code")
    state = request.GET.get("state")

    # 1. 액세스 토큰 요청
    token_url = "https://nid.naver.com/oauth2.0/token"
    token_params = {
        'grant_type': 'authorization_code',
        'client_id': settings.NAVER_CLIENT_ID,
        'client_secret': settings.NAVER_CLIENT_SECRET,
        'code': code,
        'state': state,
    }
    token_res = requests.get(token_url, params=token_params).json()
    access_token = token_res.get("access_token")

    # 2. 사용자 정보 요청
    profile_url = "https://openapi.naver.com/v1/nid/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_res = requests.get(profile_url, headers=headers).json()
    naver_info = profile_res.get("response")

    if not naver_info:
        return redirect("accounts:login")

    email = naver_info.get("email")
    name = naver_info.get("name") or naver_info.get("nickname")

    if not name:
        name = f"네이버사용자_{get_random_string(6)}"  # 최후의 보루

    # 3. email 기준으로 조회 또는 생성
    user = User.objects.filter(email=email).first()
    if not user:
        user = User.objects.create(
            email=email,
            username=name,     # ✅ 지민님 요구사항: username = name
            first_name=name,   # ✅ 사용자 표시 이름
        )

    # 4. 로그인 처리
    auth_login(request, user)
    return redirect("main:home")