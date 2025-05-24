from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings

User = get_user_model()

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.TextField()  # 리포트 요약 내용
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}님의 리포트 ({self.created_at.strftime('%Y-%m-%d')})"

class EmotionChoices(models.TextChoices):
    HAPPY = 'happy', '😊'
    NEUTRAL = 'neutral', '😐'
    SAD = 'sad', '☹️'

class Income(models.Model): # 수입
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.PositiveIntegerField()
    emotion = models.CharField(max_length=10, choices=EmotionChoices.choices, blank=True)
    
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
class Expense(models.Model): # 지출
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    amount = models.PositiveIntegerField()
    category = models.CharField(max_length=100) 
    emotion = models.CharField(max_length=10, choices=EmotionChoices.choices, blank=True)
    
class FixedExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    amount = models.PositiveIntegerField()
    day = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.amount}원 (매월 {self.day}일)"

class MonthlyBudget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    amount = models.PositiveIntegerField()  # 목표 지출액

    class Meta:
        unique_together = ('user', 'year', 'month')  # 한 달에 하나만 설정 가능

    def __str__(self):
        return f"{self.user.username} - {self.year}년 {self.month}월 목표: {self.amount}원"