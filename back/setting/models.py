from django.db import models
from django.conf import settings

class FixedExpense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # 예: '넷플릭스', '전기요금'
    amount = models.PositiveIntegerField()
    payment_day = models.IntegerField()  # 매월 며칠 (1~31)

    def __str__(self):
        return f"{self.name} - 매월 {self.payment_day}일"

