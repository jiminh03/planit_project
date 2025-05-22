from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False)  # 더 이상 고유 필요 없음
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', '남성'), ('female', '여성')], blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'  # ✅ 이메일을 로그인 식별자로 설정
    REQUIRED_FIELDS = ['username']  # ⚠️ createsuperuser 시 필수 항목

    def __str__(self):
        return self.email

class Notice(models.Model):
    title = models.CharField(max_length = 200) #제목
    content = models.TextField() #내용
    created_at = models.DateTimeField(auto_now_add=True) #등록일

    def __str__(self):
        return self.title