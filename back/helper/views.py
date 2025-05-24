from django.shortcuts import render
# Create your views here.

import os
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from openai import OpenAI
from dotenv import load_dotenv
from home.models import Expense

# GPT 기반 지출 도우미 API
class SpendingHelperView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        today = timezone.localdate()
        start_date = today - timedelta(days=14)

        expenses = Expense.objects.filter(user=request.user, date__range=(start_date, today)).order_by('-date')
        if not expenses.exists():
            return Response({"message": "최근 소비 내역이 없어 분석할 수 없습니다."})

        # 소비 내역 포맷
        lines = []
        for e in expenses:
            lines.append(f"{e.date} - {e.category} - {e.amount}원 - 감정: {e.emotion or '없음'}")

        # 프롬프트 불러오기
        load_dotenv()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_path = os.path.join(base_dir, 'helper', 'prompts', 'helper_prompt.txt')

        with open(prompt_path, encoding='utf-8') as f:
            prompt_template = f.read()

        month = today.month
        total_spent = sum(e.amount for e in expenses)

        from setting.models import FixedExpense
        from home.models import MonthlyBudget
        
        budget_obj = MonthlyBudget.objects.filter(user=request.user, year=today.year, month=today.month).first()
        if budget_obj:
            target_budget = budget_obj.budget
            budget_info = f"목표 예산: {target_budget}원"
            budget_ratio = round(abs(total_spent) / target_budget * 100, 1)
        else:
            budget_info = "목표 예산 없음"
            budget_ratio = 0

        from collections import Counter
        emotion_count = Counter(e.emotion for e in expenses if e.emotion)
        emotion_lines = "\n".join([f"{k}: {v}회" for k, v in emotion_count.items()]) if emotion_count else "감정 소비 없음"

        from collections import defaultdict
        category_sum = defaultdict(int)
        for e in expenses:
            category_sum[e.category] += abs(e.amount)
        category_lines = "\n".join([f"{k}: {v}원" for k, v in category_sum.items()])

        fixed_qs = FixedExpense.objects.filter(user=request.user)
        if fixed_qs.exists():
            fixed_lines = "\n".join([f"{f.name}: {f.amount}원 / 매월 {f.payment_day}일" for f in fixed_qs])
        else:
            fixed_lines = "고정지출 없음"
        
        prompt = prompt_template.format(
            username=request.user.username,
            month=month,
            total_spent=total_spent,
            budget_info=budget_info,
            budget_ratio=budget_ratio,
            emotion_lines=emotion_lines,
            category_lines=category_lines,
            fixed_lines=fixed_lines,
            spending_lines="\n".join(lines),
)
        # GPT 호출
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({"result": answer})
