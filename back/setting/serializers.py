# setting/serializers.py
from rest_framework import serializers
from .models import FixedExpense
from django.contrib.auth import password_validation

class FixedExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedExpense
        fields = ['id', 'user', 'name', 'amount', 'payment_day']
        read_only_fields = ['user']


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value