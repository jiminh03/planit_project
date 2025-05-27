from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # ✅ 인증 불필요
from django.utils.timezone import now
from datetime import timedelta
from collections import Counter, defaultdict
from openai import OpenAI
from dotenv import load_dotenv
import os

from django.contrib.auth import get_user_model
from home.models import Expense, MonthlyBudget
from setting.models import FixedExpense

load_dotenv()
User = get_user_model()

class SpendingHelperView(APIView):
    permission_classes = [AllowAny]  # ✅ 로그인 없이 허용

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "이메일이 필요합니다."}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "해당 이메일의 사용자를 찾을 수 없습니다."}, status=404)

        today = now().date()
        start_date = today - timedelta(days=14)
        expenses = Expense.objects.filter(user=user, date__range=(start_date, today)).order_by('-date')

        if not expenses.exists():
            return Response({"message": "최근 소비 내역이 없어 분석할 수 없습니다."})

        lines = [f"{e.date} - {e.category} - {e.amount}원 - 감정: {e.emotion or '없음'}" for e in expenses]

        # 프롬프트 불러오기
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_path = os.path.join(base_dir, 'helper', 'prompts', 'helper_prompt.txt')
        with open(prompt_path, encoding='utf-8') as f:
            prompt_template = f.read()

        total_spent = sum(e.amount for e in expenses)

        budget_obj = MonthlyBudget.objects.filter(user=user, year=today.year, month=today.month).first()
        if budget_obj:
            target_budget = budget_obj.budget
            budget_info = f"목표 예산: {target_budget}원"
            budget_ratio = round(abs(total_spent) / target_budget * 100, 1)
        else:
            budget_info = "목표 예산 없음"
            budget_ratio = 0

        emotion_count = Counter(e.emotion for e in expenses if e.emotion)
        emotion_lines = "\n".join([f"{k}: {v}회" for k, v in emotion_count.items()]) if emotion_count else "감정 소비 없음"

        category_sum = defaultdict(int)
        for e in expenses:
            category_sum[e.category] += abs(e.amount)
        category_lines = "\n".join([f"{k}: {v}원" for k, v in category_sum.items()])

        fixed_qs = FixedExpense.objects.filter(user=user)
        fixed_lines = "\n".join([f"{f.name}: {f.amount}원 / 매월 {f.payment_day}일" for f in fixed_qs]) if fixed_qs.exists() else "고정지출 없음"

        prompt = prompt_template.format(
            username=user.username,
            month=today.month,
            total_spent=total_spent,
            budget_info=budget_info,
            budget_ratio=budget_ratio,
            emotion_lines=emotion_lines,
            category_lines=category_lines,
            fixed_lines=fixed_lines,
            spending_lines="\n".join(lines),
        )

        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({"result": answer})
