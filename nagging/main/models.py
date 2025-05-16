from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.TextField()  # 리포트 요약 내용
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}님의 리포트 ({self.created_at.strftime('%Y-%m-%d')})"
