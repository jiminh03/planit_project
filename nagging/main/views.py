from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Report
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.conf import settings
import openai


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

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

@login_required
def report(request):
    user = request.user
    sample_data = "- 식비: 35%\n- 고정지출: 25%\n- 유흥비: 20%\n- 기타: 20%"
    message = f"{user.username}님의 소비 내역:\n{sample_data}\n이 소비 패턴에 대한 분석과 조언을 해줘."

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 또는 gpt-4, gpt-4o 등
        messages=[
            {"role": "system", "content": "너는 소비 데이터를 분석해주는 똑똑한 소비 컨설턴트야."},
            {"role": "user", "content": message},
        ]
    )

    gpt_reply = response.choices[0].message.content

    return render(request, 'main/report.html', {'response': gpt_reply})

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        auth_logout(request)
        return redirect('accounts:index')  # 계정 삭제 후 이동할 페이지
