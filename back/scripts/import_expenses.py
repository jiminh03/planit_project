import pandas as pd
from django.conf import settings
import os
import sys
import django

# Django 환경 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit.settings')
django.setup()

from home.models import Expense
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(email='admin@naver.com')  # ⚠️ 이메일 수정 필요

# 엑셀 파일 경로
file_path = 'test_cases/testuser1.xlsx'  # .xlsx 확장자 확인

# 데이터 불러오기
df = pd.read_excel(file_path)

# 데이터프레임 열 예시: date, amount, category, emotion
for idx, row in df.iterrows():
    Expense.objects.create(
        user=user,
        date=row['날짜'],
        amount=row['금액'],
        category=row['카테고리'],
        emotion=row.get('감정', '')  # 선택적
    )

print("✅ 지출 데이터 DB 저장 완료")