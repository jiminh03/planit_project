from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth import logout as auth_logout
from .models import Notice
from django.core.paginator import Paginator

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
