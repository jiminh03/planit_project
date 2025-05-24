from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from home.models import MonthlyBudget
from home.serializers import MonthlyBudgetSerializer  # 필요 시 settings로 옮겨도 됨
from .models import FixedExpense
from rest_framework import serializers
from .serializers import FixedExpenseSerializer, PasswordChangeSerializer
from datetime import timedelta, datetime, date
from calendar import monthrange
from django.contrib.auth import authenticate

# 월 목표 예산 설정
class MonthlyBudgetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MonthlyBudgetSerializer(data=request.data)
        if serializer.is_valid():
            MonthlyBudget.objects.filter(
                user=request.user,
                year=serializer.validated_data['year'],
                month=serializer.validated_data['month']
            ).delete()
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        if not year or not month:
            return Response({'error': 'year와 month를 지정해주세요.'}, status=400)

        try:
            budget = MonthlyBudget.objects.get(user=request.user, year=year, month=month)
        except MonthlyBudget.DoesNotExist:
            budget = MonthlyBudget.objects.filter(user=request.user).order_by('-year', '-month').first()
            if not budget:
                return Response({'error': '등록된 예산이 없습니다.'}, status=404)

        serializer = MonthlyBudgetSerializer(budget)
        return Response(serializer.data)
    
# 고정 지출 등록 / 조회
class FixedExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FixedExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        expenses = FixedExpense.objects.filter(user=request.user).order_by('payment_day')
        serializer = FixedExpenseSerializer(expenses, many=True)
        return Response(serializer.data)


# 예상 소비 예정 항목 조회 (홈 화면에 필요하면 사용, 고정 지출 날짜까지 얼마나 남았는지?..)
class PredictedFixedExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        base_date_str = request.query_params.get('date')
        if not base_date_str:
            return Response({'error': '기준 날짜를 YYYY-MM-DD 형식으로 전달해주세요. (?date=2025-06-01)'}, status=400)

        try:
            base_date = datetime.strptime(base_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({'error': '날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식이어야 합니다.'}, status=400)

        user = request.user

        expenses = FixedExpense.objects.filter(user=user)
        results = []

        for expense in expenses:
            year, month = base_date.year, base_date.month

            # 기준일보다 지출일이 작으면 다음 달로 이월
            if expense.payment_day < base_date.day:
                if month == 12:
                    year += 1
                    month = 1
                else:
                    month += 1

            # 월 최대 일 수 고려
            last_day = monthrange(year, month)[1]
            day = min(expense.payment_day, last_day)

            try:
                scheduled_date = date(year, month, day)
            except ValueError:
                continue

            if abs((scheduled_date - base_date).days) <= 3:
                results.append({
                    "name": expense.name,
                    "amount": expense.amount,
                    "scheduled_for": str(scheduled_date)
                })

        return Response(results)

# 비밀번호 변경
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({'old_password': ['현재 비밀번호가 올바르지 않습니다.']}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'detail': '비밀번호가 성공적으로 변경되었습니다.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)