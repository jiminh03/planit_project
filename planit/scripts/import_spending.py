import os
import sys
import django
import pandas as pd

# ✅ 1. Django 설정을 위한 경로 추가
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(ROOT_DIR)

# ✅ 2. Django 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planit.settings")
django.setup()

# ✅ 3. 모델 불러오기
from main.models import Expense  # 또는 Spending 모델명을 정확히 사용하세요
from django.contrib.auth import get_user_model

# ✅ 4. 타겟 유저 가져오기
User = get_user_model()
target_user = User.objects.get(email="jamieh200203@gmail.com")

# ✅ 5. 엑셀 불러오기
excel_path = os.path.join(ROOT_DIR, "소비_황지민.xlsx")
df = pd.read_excel(excel_path)

# ✅ 6. 데이터 저장
for _, row in df.iterrows():
    try:
        raw_amount = row['금액']
        amount = int(raw_amount)

        if amount <= 0:
            print(f"🚫 건너뜀 (0 이하 금액): {raw_amount}")
            continue

        Expense.objects.create(
            user=target_user,
            date=pd.to_datetime(row['날짜']).date(),
            amount=amount,
            category=str(row['카테고리']).strip()
        )
    except Exception as e:
        print(f"❌ 오류 발생: {e} (원시 금액: {row['금액']})")


print("✅ 엑셀 데이터가 jamieh200203@gmail.com 계정에 저장되었습니다.")
