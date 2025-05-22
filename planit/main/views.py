from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Report
from django.contrib.auth import logout as auth_logout
from django.conf import settings
import openai
import markdown
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Expense, Income
from .serializers import ExpenseSerializer, IncomeSerializer
from datetime import date, datetime
from .models import Expense
from django.shortcuts import get_object_or_404
import csv
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from .forms import FixedExpenseForm
from .forms import MonthlyBudgetForm
from .models import MonthlyBudget
from django.db.models import Sum, Count
import re

@login_required
def home(request):
    user = request.user
    today = date.today()
    latest_report = Report.objects.filter(user=user).order_by('-created_at').first()
    expenses = Expense.objects.filter(user=user).order_by('-date', '-id')
    todays_expenses = Expense.objects.filter(user=request.user, date=today)


    context = {
        'user': user,
        'report': latest_report,
        'expenses': expenses,
        'todays_expenses': todays_expenses,
        "today":today,
    }
    return render(request, 'main/home.html', context)


def helper(request):
    return render(request, 'main/helper.html')

def setting(request):
    return render(request, 'main/setting.html')

# 내 소비 분석 GPT 결과

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

# 메뉴 키 → 라벨 매핑
MENU_ITEMS = {
    "summary": "한 줄 분석",
    "pattern": "소비 패턴 분석",
    "daily": "날짜별 소비 패턴",
    "emotion": "감정-소비 관계",
    "category": "카테고리별 분석",
    "tendency": "소비 성향 진단",
    "feedback": "개인 맞춤형 피드백",
}


@login_required
def report(request):
    user = request.user
    today = date.today()
    month_str =f"{today.month}월"
    analysis_type = request.GET.get("type", "summary")  # default: summary

    # 📊 1. 이번 달 소비 데이터
    expenses = Expense.objects.filter(
        user=user,
        date__year=today.year,
        date__month=today.month
    )

    # 총 지출
    total_spent = expenses.aggregate(total=Sum("amount"))["total"] or 0

    # 카테고리별 집계
    by_category = expenses.values("category").annotate(total=Sum("amount")).order_by("-total")
    category_lines = "\n".join([f"- {c['category']}: {c['total']}원" for c in by_category])

    # 감정별 집계
    by_emotion = expenses.values("emotion").annotate(total=Sum("amount")).order_by("-total")
    emotion_lines = "\n".join([f"- {e['emotion']}: {e['total']}원" for e in by_emotion])

    # 📎 2. System message
    system_message = {
        "role": "system",
        "content": (
            "너는 소비 분석 전문가이자 감정 소비 상담사야. "
            "사용자의 소비 데이터를 분석해서 요약, 성향 진단, 피드백을 제공하는 역할이야. "
            "친절하고 분석적인 어조로, 실질적인 조언을 해줘."
        )
    }

    # 📋 3. 프롬프트 유형별 구성
    prompts = {
        "summary": f"""
{user.username}님의 {month_str}월 소비 분석 요약입니다.

총 지출: {total_spent}원

[카테고리별 지출]
{category_lines}

[감정별 지출]
{emotion_lines}

아래의 각 항목마다 2~3문단 정도로 상세히 분석해줘.
비교 수치, 추천 행동, 예시 등을 포함해줘.
1. 월 지출 총액
2. 목표 예산 대비 비율 (예산 데이터는 없지만, 상식선에서 언급 가능)
3. 소비 성향 (예: 절약형, 감정소비형 등)
4. 핵심 조언 문장 (예: '주말 약속을 줄여보세요')
""",

        "emotion": f"""
{user.username}님의 {month_str}월 감정 기반 소비 데이터를 분석해줘.

[감정별 소비]
{emotion_lines}

각 감정이 소비에 어떤 영향을 미치는지 분석하고,
가장 지출이 큰 감정 상태를 진단해줘.
마지막엔 개선 팁을 2줄로 요약해줘.
""",

        "tendency": f"""
{user.username}님의 소비 패턴을 기반으로 성향을 분석해줘.

[카테고리별 소비]
{category_lines}

[감정별 소비]
{emotion_lines}

이 사람은 어떤 소비 성향을 보이고 있고, 어떤 특징이 있는지 3가지로 요약해줘.
과소비형 / 절약형 / 감정소비형 중 하나로 판단해줘.
마지막에 '지출 개선 포인트'를 하나 제시해줘.
""",

        "pattern": f"""
{user.username}님의 소비 흐름을 분석해줘.

[카테고리별 소비]
{category_lines}

[감정별 소비]
{emotion_lines}

요일/시간대/감정이 소비에 어떤 영향을 주는지 예측하고,
반복되는 소비 습관이 있다면 진단해줘.
""",

        "feedback": f"""
{user.username}님의 소비 데이터를 바탕으로 개인화된 피드백을 줘.

총 지출: {total_spent}원

[카테고리별 소비]
{category_lines}

[감정별 소비]
{emotion_lines}

소비를 줄이기 위한 실천 팁을 2~3개 제시하고,
전체적으로 어떤 지출을 줄이면 효과적일지도 알려줘.
"""
    }

    user_message = {
        "role": "user",
        "content": prompts.get(analysis_type, prompts["summary"])
    }

    # ✅ GPT 호출
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_message, user_message],
        max_tokens=1024,
    )

    # GPT 응답 결과
    raw = response.choices[0].message.content

    # ✅ "숫자. 제목" 패턴 기준으로 항목 분리 (예: "1. 월 지출 총액")
    blocks = re.split(r'(?=^###\s*\d+\.\s)', raw.strip(), flags=re.MULTILINE)

    cards = []
    for block in blocks:
        if block.strip():
            html = markdown.markdown(
                block.strip(),
                extensions=["extra", "toc"]
            )
            cards.append({'html': html})


    return render(request, "main/report.html", {
        "menu_items": ["summary", "emotion", "tendency", "pattern", "feedback"],
        "current": analysis_type,
        "cards": cards,
    })



@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        auth_logout(request)
        return redirect('accounts:index')  # 계정 삭제 후 이동할 페이지


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
@login_required
def create_expense(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        emotion = request.POST.get("emotion")
        selected_date = request.POST.get("date", date.today())  # 기본 오늘
        Expense.objects.create(
            user=request.user,
            amount=amount,
            category=category,
            emotion=emotion,
            date=selected_date,
        )
    return redirect("main:home")

@login_required
def create_income(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        emotion = request.POST.get("emotion")
        selected_date = request.POST.get("date", date.today())
        Income.objects.create(
            user=request.user,
            amount=amount,
            emotion=emotion,
            date=selected_date,
        )
    return redirect("main:home")

@login_required
def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.amount = request.POST.get('amount')
        expense.category = request.POST.get('category')
        expense.emotion = request.POST.get('emotion')
        expense.save()
        return redirect('main:home')
    return render(request, 'main/edit_expense.html', {'expense': expense})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    return redirect('main:home')

@login_required
def download_expense_data(request):
    user = request.user
    expenses = Expense.objects.filter(user=user)

    response = HttpResponse(content_type='text/csv')
    filename = f"{user.username}_소비데이터_{datetime.now().strftime('%Y%m%d')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{escape_uri_path(filename)}"'
    response.write(u'\ufeff'.encode('utf8'))  # UTF-8 BOM for Excel

    writer = csv.writer(response)
    writer.writerow(['날짜', '금액', '카테고리', '감정'])

    for expense in expenses:
        writer.writerow([
            expense.date.strftime('%Y-%m-%d'),
            expense.amount,
            expense.category,
            expense.emotion,
        ])

    return response

@login_required
def fixed_expense_input(request):
    if request.method == 'POST':
        form = FixedExpenseForm(request.POST)
        if form.is_valid():
            fixed = form.save(commit=False)
            fixed.user = request.user
            fixed.save()
            return redirect('main:setting')  # 설정 페이지로 리디렉션
    else:
        form = FixedExpenseForm()
    return render(request, 'main/fixed_expense_input.html', {'form': form})

@login_required
def monthly_budget_view(request):
    user = request.user
    if request.method == 'POST':
        form = MonthlyBudgetForm(request.POST)
        if form.is_valid():
            budget, created = MonthlyBudget.objects.update_or_create(
                user=user,
                year=form.cleaned_data['year'],
                month=form.cleaned_data['month'],
                defaults={'amount': form.cleaned_data['amount']}
            )
            return redirect('main:setting')
    else:
        form = MonthlyBudgetForm()

    return render(request, 'main/monthly_budget.html', {'form': form})