from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
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
    permission_classes = [AllowAny]

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

        # ✅ 프롬프트 템플릿 파일 경로 정의
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompt_dir = os.path.join(base_dir, 'helper', 'prompts')
        prompt_files = {
            "summary": "prompt_summary.txt",
            "strategy": "prompt_strategy.txt",
            "fixed": "prompt_fixed.txt",
            "simulation": "prompt_simulation.txt",
        }

        # ✅ 파일 불러오기
        try:
            templates = {}
            for key, filename in prompt_files.items():
                with open(os.path.join(prompt_dir, filename), encoding='utf-8') as f:
                    templates[key] = f.read()
        except FileNotFoundError as e:
            return Response({"error": f"프롬프트 파일 누락: {str(e)}"}, status=500)

        # ✅ 데이터 포맷팅
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
        emotion_lines = "\n".join([f"{k}: {v}회" for k, v in emotion_count.items()]) or "감정 소비 없음"

        category_sum = defaultdict(int)
        for e in expenses:
            category_sum[e.category] += abs(e.amount)
        category_lines = "\n".join([f"{k}: {v}원" for k, v in category_sum.items()]) or "카테고리 정보 없음"

        fixed_qs = FixedExpense.objects.filter(user=user)
        fixed_lines = "\n".join([
            f"{f.name}: {f.amount}원 / 매월 {f.payment_day}일" for f in fixed_qs
        ]) if fixed_qs.exists() else "고정지출 없음"

        # ✅ 공통 context 정의 (txt 파일 대신 코드 내에서 생성)
        context = f"""
다음은 사용자의 월간 소비 분석 요청입니다.
사용자 이름: {user.username}
분석 월: {today.month}
총 지출: {total_spent}원
{budget_info}
예산 대비 비율: {budget_ratio}%

[감정별 소비]
{emotion_lines}

[카테고리별 소비]
{category_lines}

[고정지출 항목]
{fixed_lines}
""".strip()

        format_kwargs = {
            "context": context,
            "username": user.username,
            "month": today.month,
            "total_spent": total_spent,
            "budget_info": budget_info,
            "budget_ratio": budget_ratio,
            "emotion_lines": emotion_lines,
            "category_lines": category_lines,
            "fixed_lines": fixed_lines,
            "spending_lines": "\n".join(lines),
        }

        # ✅ GPT 호출
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            results = {}

            for key in ["summary", "strategy", "fixed", "simulation"]:
                filled_prompt = templates[key].format(**format_kwargs)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": filled_prompt}],
                    max_tokens=1800,
                    temperature=0.7,
                )
                results[f"{key}_result"] = response.choices[0].message.content.strip()

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response(results)
    
