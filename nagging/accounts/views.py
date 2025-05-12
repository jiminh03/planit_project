from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Notice
from django.core.paginator import Paginator

def index(request):
    return render(request, 'accounts/index.html')

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return redirect('main:home')

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/signup.html', context)

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