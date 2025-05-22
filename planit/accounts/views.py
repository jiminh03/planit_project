from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, login as auth_login
from .forms import CustomUserCreationForm
from django.contrib.auth import logout as auth_logout
from .models import Notice
from django.core.paginator import Paginator
import os, requests
import urllib.parse
from uuid import uuid4


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
    }
    return render(request, 'accounts/login.html', context)

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
