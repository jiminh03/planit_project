from django.db import models
from django.conf import settings

class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.PositiveIntegerField()
    source = models.CharField(max_length=100)
    emotion = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.date} - {self.amount}원 ({self.source})"


class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.IntegerField()
    category = models.CharField(max_length=100)
    emotion = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.date} - {self.amount}원 ({self.category})"

class MonthlyBudget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    budget = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'year', 'month')

    def __str__(self):
        return f"{self.year}년 {self.month}월 - ₩{self.budget}"