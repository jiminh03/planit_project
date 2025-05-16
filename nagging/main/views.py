from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Report
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.conf import settings
import openai
import markdown


@login_required
def home(request):
    user = request.user
    latest_report = Report.objects.filter(user=user).order_by('-created_at').first()

    context = {
        'user': user,
        'report': latest_report,
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
    analysis_type = request.GET.get("type", "pattern")
    sample_data = "- 식비: 35%\n- 고정지출: 25%\n- 유흥비: 20%\n- 기타: 20%"

    system_message = {
        "role": "system",
        "content": "너는 소비 데이터를 분석해주는 똑똑한 소비 컨설턴트야."
    }

    # 각 타입별 GPT 프롬프트
    prompts = {
        "summary": f"{user.username}님의 소비 내역:\n{sample_data}\n한 줄로 요약해줘. 핵심만 간단히 말해줘.",
        "pattern": f"{user.username}님의 소비 내역:\n{sample_data}\n이 소비 패턴을 분석해줘. 어떤 성향이 보이는지 알려줘.",
        "daily": (
            f"{user.username}님의 날짜별 소비 내역:\n"
            "- 5월 1일: 식비 30%\n"
            "- 5월 2일: 고정지출 40%\n"
            "- 5월 3일: 유흥비 50%\n"
            "이 데이터를 바탕으로 날짜별 소비 패턴의 변화나 반복되는 경향이 있는지 분석해줘."
        ),
        "emotion": (
            f"{user.username}님의 소비 및 감정 내역:\n"
            "- 행복할 때: 유흥비 증가\n"
            "- 우울할 때: 쇼핑 비용 증가\n"
            "이러한 감정과 소비의 연관성을 분석하고, 개선 방향을 제시해줘."
        ),
        "category": f"{user.username}님의 소비 내역:\n{sample_data}\n각 항목(식비, 고정지출, 유흥비, 기타)에 대해 자세히 분석해줘. 특징과 개선점이 있다면 알려줘.",
        "tendency": f"{user.username}님의 소비 내역:\n{sample_data}\n이 소비 내역을 바탕으로 소비 성향을 진단해줘. 예를 들면 과소비형, 절약형, 감정소비형 등으로.",
        "feedback": f"{user.username}님의 소비 내역:\n{sample_data}\n개인 맞춤형 피드백을 줘. 예산 계획, 절약 팁, 우선순위 조정 등 실천 가능한 조언 위주로 알려줘.",
    }

    user_content = prompts.get(analysis_type, prompts["pattern"])
    user_message = {"role": "user", "content": user_content}

    # GPT 요청 (max_tokens 충분히!)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_message, user_message],
        max_tokens=1024,
    )
    raw = response.choices[0].message.content
    result_html = markdown.markdown(raw, extensions=["extra"])
    
    print("현재 분석 타입:", analysis_type)
    print("프롬프트:", user_content)


    return render(request, "main/report.html", {
        "menu_items": MENU_ITEMS,
        "current": analysis_type,
        "result": result_html,
    })

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        auth_logout(request)
        return redirect('accounts:index')  # 계정 삭제 후 이동할 페이지
