from django import forms
from .models import FixedExpense
from .models import MonthlyBudget
import datetime

class FixedExpenseForm(forms.ModelForm):
    class Meta:
        model = FixedExpense
        fields = ['name', 'amount', 'date']
        labels = {
            'name': '항목명',
            'amount': '금액',
            'date': '납부일',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class MonthlyBudgetForm(forms.ModelForm):
    class Meta:
        model = MonthlyBudget
        fields = ['year', 'month', 'amount']
        labels = {
            'year': '년도',
            'month': '월',
            'amount': '목표 지출액 (원)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = datetime.datetime.now()
        self.fields['year'].initial = now.year
        self.fields['month'].initial = now.month