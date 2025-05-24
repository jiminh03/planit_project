from django.template.loader import render_to_string
from django.conf import settings
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from collections import Counter, defaultdict
from home.models import Expense
from dotenv import load_dotenv
from openai import OpenAI


class SpendingReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        start_date = today.replace(day=1)

        expenses = Expense.objects.filter(user=request.user, date__range=(start_date, today))

        total_spent = sum(abs(e.amount) for e in expenses)
        emotion_count = Counter(e.emotion for e in expenses if e.emotion)
        category_sum = defaultdict(int)
        for e in expenses:
            category_sum[e.category] += abs(e.amount)

        # 프롬프트 템플릿 경로 설정 및 로드
        prompt_path = os.path.join(settings.BASE_DIR, 'report', 'prompts', 'report_prompt.txt')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()

        try:
            emotion_lines = "\n".join(f"{emotion}: {count}회" for emotion, count in emotion_count.items()) if emotion_count else "없음"
            category_lines = "\n".join(f"{category}: {amount}원" for category, amount in category_sum.items()) if category_sum else "없음"

            prompt = prompt_template.format(
                username=request.user.username,
                year=today.year,
                month=today.month,
                emotion_lines=emotion_lines,
                category_lines=category_lines,
                total_spent=total_spent,
                budget_info="(예산 정보가 설정되어 있지 않습니다.)",
                budget_ratio="(지출 대비 예산 비율 정보가 없습니다.)"
            )
        except KeyError as e:
            return Response({"error": f"프롬프트 구성 중 누락된 항목이 있습니다: {str(e)}"}, status=500)

        # .env 파일에서 환경변수 로드
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return Response({"error": "OPENAI_API_KEY 환경변수가 설정되어 있지 않습니다."}, status=500)

        client = OpenAI(api_key=api_key)

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "너는 소비 분석을 도와주는 분석가야."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.7
            )
            analysis = response.choices[0].message.content.strip()
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({
            "result": analysis
        })