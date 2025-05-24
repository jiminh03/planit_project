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
from django.http import HttpResponse, JsonResponse
from django.utils.encoding import escape_uri_path
from .forms import FixedExpenseForm
from .forms import MonthlyBudgetForm
from .models import MonthlyBudget, FixedExpense
from django.db.models import Sum, Count
import re
from django.contrib import messages

def home(request):
    today = date.today()

    if request.user.is_authenticated:
        user = request.user
        latest_report = Report.objects.filter(user=user).order_by('-created_at').first()
        expenses = Expense.objects.filter(user=user).order_by('-date', '-id')  # 전체 지출
        todays_expenses = expenses  # 변수명만 유지하고 전체 할당
    else:
        user = None
        latest_report = None
        expenses = Expense.objects.filter(user__isnull=True).order_by('-date', '-id')  # 익명 사용자용
        todays_expenses = expenses

    context = {
        'user': user,
        'report': latest_report,
        'expenses': expenses,
        'todays_expenses': todays_expenses,
        "today": today,
    }
    return render(request, 'main/home.html', context)




def report(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    user = request.user
    today = date.today()
    year = today.year
    month = today.month
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

    # ✅ 현재 월 목표 예산 조회
    try:
        budget = MonthlyBudget.objects.get(user=user, year=year, month=month)
        target_budget = budget.amount
    except MonthlyBudget.DoesNotExist:
        target_budget = None
        
    # 📎 2. System message
    system_message = {
        "role": "system",
        "content": (
            "너는 소비 분석 전문가이자 감정 소비 상담사야. "
            "사용자의 소비 데이터를 분석해서 요약, 성향 진단, 피드백을 제공하는 역할이야. 사용자가 참고할 수 있는 내용이 많게, 내용은 최대한 많이 작성해줘."
            "친절하고 분석적인 어조로, 실질적인 조언을 해줘."
        )
    }
    
    budget_line = ""
    if target_budget:
        percent = round(total_spent / target_budget * 100) if target_budget > 0 else 0
        budget_line = (
            f"설정된 목표 예산: {target_budget}원\n"
            f"총 지출: {total_spent}원\n"
            f"예산 대비 지출 비율: 약 {percent}%\n"
        )
    else:
        budget_line = "※ 목표 예산 정보가 설정되지 않았습니다.\n"

    prompts = {
        "summary": f"""
    {user.username}님의 {month_str}월 소비 분석 요약입니다.

    {budget_line}

    [카테고리별 지출]
    {category_lines}

    [감정별 지출]
    {emotion_lines}

    아래 4가지 항목을 각각 자세하고 길게 분석해줘. 항목마다 소제목 붙이고 구분해줘.
    근데 적절하게 이모티콘도 붙여가면서 예쁘게 대답해줬으면 좋겠어.
    비교 수치, 추천 행동, 예시 등을 포함해줘.
    
    1. 월 지출 총액
    2. 목표 예산 대비 비율
    3. 소비 성향 (예: 절약형, 감정소비형 등)
    4. 핵심 조언 문장 (예: '주말 약속을 줄여보세요')
    """,

        "emotion": f"""
{user.username}님의 {month_str}월 감정 기반 소비 데이터를 분석해줘.

[감정별 소비]
{emotion_lines}

각 감정이 소비에 어떤 영향을 미치는지 분석하고,
가장 지출이 큰 감정 상태를 진단해줘.
마지막엔 개선 팁을 요약해줘.
""",

        "tendency": f"""
{user.username}님의 소비 패턴을 기반으로 성향을 분석해줘.

[카테고리별 소비]
{category_lines}

[감정별 소비]
{emotion_lines}

이 사람은 어떤 소비 성향을 보이고 있고, 어떤 특징이 있는지 3가지로 나타내줘.
과소비형 / 절약형 / 안정형 중 하나로 판단해줘.
마지막에 '지출 개선 포인트'를 하나 제시해줘.
""",

        "pattern": f"""
{user.username}님의 소비 흐름을 분석해줘.

[카테고리별 소비]
{category_lines}

[감정별 소비]
{emotion_lines}

요일/시간대/감정이 소비에 어떤 영향을 주는지 예측하고,
기복형 / 안정형 중 하나로 판단해줘.
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
    
    
def helper(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    user = request.user
    today = date.today()
    year = today.year
    month = today.month

    expenses = Expense.objects.filter(user=user, date__year=year, date__month=month)
    total_spent = expenses.aggregate(total=Sum("amount"))["total"] or 0
    by_emotion = expenses.values("emotion").annotate(total=Sum("amount")).order_by("-total")
    by_category = expenses.values("category").annotate(total=Sum("amount")).order_by("-total")

    # 월 예산
    try:
        budget = MonthlyBudget.objects.get(user=user, year=year, month=month)
        target_budget = budget.amount
        budget_ratio = round(total_spent / target_budget * 100) if target_budget > 0 else "정보 없음"
    except MonthlyBudget.DoesNotExist:
        target_budget = None
        budget_ratio = "정보 없음"
        
    # 고정지출 항목 조회
    fixed_expenses = FixedExpense.objects.filter(user=user).order_by('day')
    fixed_lines = "\n".join([
        f"- {fe.name}: {fe.amount}원 (매월 {fe.day}일)" for fe in fixed_expenses
    ]) or "등록된 고정지출 항목이 없습니다."

    emotion_lines = "\n".join([f"- {e['emotion']}: {e['total']}원" for e in by_emotion])
    category_lines = "\n".join([f"- {c['category']}: {c['total']}원" for c in by_category])

    system_message = {
        "role": "system",
        "content": (
            "너는 가계부 기반 소비 절약 도우미야. "
            "사용자의 소비 내역을 분석해서 절약 전략, 정기지출 정리, 감정 소비 개선, 절약 시뮬레이션을 제공하는 역할이야. 사용자가 참고할 수 있는 내용이 많아지도록 최대한 많은 내용을 담아줘."
            "실질적이고 명확한 문장으로 구성해줘."
        )
    }

    user_prompt = f"""
{user.username}님의 {month}월 소비 내역을 기반으로 지출 도우미 분석을 해줘.

총 지출: {total_spent}원
{"목표 예산: " + str(target_budget) + "원" if target_budget else "목표 예산 없음"}
예산 대비 비율: {budget_ratio}%

[감정별 소비]
{emotion_lines}

[카테고리별 소비]
{category_lines}

[고정지출 항목]
{fixed_lines}

아래 4가지 항목을 각각 자세하고 길게 분석해줘. 항목마다 소제목 붙이고 구분해줘.
근데 적절하게 이모티콘도 붙여가면서 예쁘게 대답해줬으면 좋겠어.

1. 개선이 필요한 소비 패턴 요약 (감정소비, 특정 시간대, 계획 외 소비 등)
2. 대체 전략 제안 (불필요 소비 줄이기, 감정소비 대처 팁 등)
3. 정기지출 정리 제안 (정기구독 목록 예시 + 해지 or 요금제 조정 제안)
4. 절약 시뮬레이션 (전략 요약, 예상 절약 금액, 실행 트리거 등)
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_message, {"role": "user", "content": user_prompt}],
        max_tokens=1024,
    )

    raw = response.choices[0].message.content
    blocks = re.split(r'(?=^###\s*\d+\.\s)', raw.strip(), flags=re.MULTILINE)

    cards = []
    for block in blocks:
        if block.strip():
            html = markdown.markdown(block.strip(), extensions=["extra", "toc"])
            cards.append({'html': html})

    return render(request, "main/helper.html", {
        "cards": cards,
        "menu_items": ["pattern", "strategy", "subscriptions", "simulation"],
        "current": "summary",
    })


def setting(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
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
def delete_account(request):
    if request.method == "POST":
        password = request.POST.get("password")
        user = request.user
        if user.check_password(password):
            user.delete()
            auth_logout(request)
            return redirect("accounts:index")
        else:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            return redirect("main:delete_confirm")
    return render(request, "main/delete_confirm.html")


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
            return redirect('main:fixed_expense_input')
    else:
        form = FixedExpenseForm()

    expenses = FixedExpense.objects.filter(user=request.user).order_by('day')
    return render(request, 'main/fixed_expense_input.html', {
        'form': form,
        'expenses': expenses,
    })


@login_required
def monthly_budget_view(request):
    user = request.user
    now = datetime.now()
    year = now.year
    month = now.month

    # 현재 연도/월에 해당하는 기존 예산 찾기
    try:
        budget = MonthlyBudget.objects.get(user=user, year=year, month=month)
    except MonthlyBudget.DoesNotExist:
        budget = None

    if request.method == 'POST':
        form = MonthlyBudgetForm(request.POST, instance=budget)
        if form.is_valid():
            new_budget = form.save(commit=False)
            new_budget.user = user
            new_budget.save()
            return redirect('main:setting')
    else:
        form = MonthlyBudgetForm(instance=budget)

    return render(request, 'main/monthly_budget.html', {'form': form})

def calendar_data(request):
    today = datetime.now()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # 로그인 여부에 따라 사용자 필터링
    if request.user.is_authenticated:
        expenses = Expense.objects.filter(user=request.user, date__year=year, date__month=month)
        incomes = Income.objects.filter(user=request.user, date__year=year, date__month=month)
    else:
        # 로그인하지 않은 경우에도 빈 응답이 아니라 모든 공개 데이터 내려줌 (프로토타입 단계)
        expenses = Expense.objects.filter(date__year=year, date__month=month)
        incomes = Income.objects.filter(date__year=year, date__month=month)

    data = {}

    for e in expenses:
        day = e.date.isoformat()
        data.setdefault(day, []).append({
            "type": "expense",
            "amount": e.amount,
            "category": e.category,
            "emotion": e.emotion
        })

    for i in incomes:
        day = i.date.isoformat()
        data.setdefault(day, []).append({
            "type": "income",
            "amount": i.amount,
            "source": getattr(i, 'source', '기타'),
            "emotion": i.emotion
        })

    return JsonResponse(data)
