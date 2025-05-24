from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', '남성'), ('female', '여성')], blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'  # 이메일을 로그인 ID로 사용
    REQUIRED_FIELDS = ['username']  # createsuperuser 시 추가 입력 필드