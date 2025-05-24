from collections import defaultdict
from django.db.models import Sum
from calendar import monthrange
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Income, Expense
from .serializers import IncomeSerializer, ExpenseSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView

# CSRF exemption for login view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# 수입 등록
class IncomeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incomes = Income.objects.filter(user=request.user)
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if year and month:
            incomes = incomes.filter(date__year=year, date__month=month)

        incomes = incomes.order_by('-date')
        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 지출 등록
class ExpenseListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if year and month:
            expenses = expenses.filter(date__year=year, date__month=month)

        expenses = expenses.order_by('-date')
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 특정 날짜를 클릭했을 때 필요한 기능 (날짜별 조회)
class TransactionByDateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({'error': '날짜를 지정해주세요.'}, status=400)

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': '날짜 형식은 YYYY-MM-DD 이어야 합니다.'}, status=400)

        incomes = Income.objects.filter(user=request.user, date=date_obj)
        expenses = Expense.objects.filter(user=request.user, date=date_obj)

        income_data = IncomeSerializer(incomes, many=True).data
        expense_data = ExpenseSerializer(expenses, many=True).data

        return Response({
            'incomes': income_data,
            'expenses': expense_data,
        })
    
# 수입 항목 상세 조회/수정/삭제
class IncomeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

# 지출 항목 상세 조회/수정/삭제
class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


# 월 단위 요약 API (날짜별 수입/지출 총액 표시할 때 사용)
class MonthlySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if not year or not month:
            return Response({'error': 'year와 month를 지정해주세요.'}, status=400)

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({'error': 'year와 month는 정수여야 합니다.'}, status=400)

        # 해당 월의 시작일과 종료일 계산
        start_date = datetime(year, month, 1).date()
        last_day = monthrange(year, month)[1]
        end_date = datetime(year, month, last_day).date()

        # 날짜별로 집계
        income_by_date = Income.objects.filter(
            user=request.user, date__range=(start_date, end_date)
        ).values('date').annotate(total_income=Sum('amount'))

        expense_by_date = Expense.objects.filter(
            user=request.user, date__range=(start_date, end_date)
        ).values('date').annotate(total_expense=Sum('amount'))

        result = defaultdict(lambda: {"income_total": 0, "expense_total": 0})

        for item in income_by_date:
            result[str(item['date'])]["income_total"] = item['total_income']

        for item in expense_by_date:
            result[str(item['date'])]["expense_total"] = item['total_expense']

        return Response(result)
    
# 월간 소비/수입 통계 요약 (월 전체 총지출, 총수입, 감정별 소비 비율, 카테고리별 지출 분석 등)
class MonthlySummaryStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if not year or not month:
            return Response({'error': 'year와 month를 지정해주세요.'}, status=400)

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({'error': 'year와 month는 정수여야 합니다.'}, status=400)

        # 해당 월의 시작일과 종료일 계산
        start_date = datetime(year, month, 1).date()
        last_day = monthrange(year, month)[1]
        end_date = datetime(year, month, last_day).date()

        incomes = Income.objects.filter(user=request.user, date__range=(start_date, end_date))
        expenses = Expense.objects.filter(user=request.user, date__range=(start_date, end_date))

        total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
        total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0

        # 카테고리별 지출 집계
        category_data = expenses.values('category').annotate(total=Sum('amount')).order_by('-total')
        top_categories = {item['category']: item['total'] for item in category_data}

        # 감정 분포 집계
        emotion_data = expenses.values('emotion').annotate(count=Sum(1)).order_by('-count')
        emotion_distribution = {item['emotion']: item['count'] for item in emotion_data if item['emotion']}

        return Response({
            'total_income': total_income,
            'total_expense': total_expense,
            'top_categories': top_categories,
            'emotion_distribution': emotion_distribution,
        })


# 오늘 지출 및 목표 예산 기반 하루 권장 지출액 반환 API
from django.utils import timezone
from home.models import MonthlyBudget  # 해당 모델이 home/models.py에 있어야 합니다

class TodaySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        year = today.year
        month = today.month

        expenses_today = Expense.objects.filter(user=request.user, date=today)
        total_expense = expenses_today.aggregate(total=Sum('amount'))['total'] or 0

        # 목표 예산 가져오기
        try:
            budget_obj = MonthlyBudget.objects.get(user=request.user, year=year, month=month)
            daily_recommendation = budget_obj.budget // monthrange(year, month)[1]
        except MonthlyBudget.DoesNotExist:
            daily_recommendation = None

        return Response({
            'date': str(today),
            'total_expense': total_expense,
            'recommended_daily_budget': daily_recommendation,
        })

# 홈화면에 띄울 AI 피드백
class AIFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        import openai
        import os
        from dotenv import load_dotenv
        from openai import OpenAI

        # 최근 지출 내역을 받아옴
        expenses = Expense.objects.filter(user=request.user).order_by('-date')[:20]
        lines = []
        for exp in expenses:
            line = f"{exp.date} - {exp.category} - {exp.amount}원 - 감정: {exp.emotion or '없음'}"
            lines.append(line)

        # 프롬프트 외부 파일로부터 불러오기
        load_dotenv()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_path = os.path.join(base_dir, 'home', 'prompts', 'ai_feedback_prompt.txt')

        with open(prompt_path, encoding='utf-8') as f:
            prompt_template = f.read()

        prompt = prompt_template.format(spending_lines="\n".join(lines))

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({'feedback': answer})


# 임시 CSRF exempt 로그인 뷰 (실제 구현 내용으로 대체 필요)
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        # 이 부분은 실제 구현 내용으로 대체되어야 합니다
        return Response({'message': 'CSRF exempt login view placeholder'}, status=200)