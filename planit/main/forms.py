from django import forms
from .models import FixedExpense
from .models import MonthlyBudget
import datetime

class FixedExpenseForm(forms.ModelForm):
    class Meta:
        model = FixedExpense
        fields = ['name', 'amount', 'day']
        labels = {
            'name': '항목명',
            'amount': '금액',
            'day': '납부일(매월)',
        }

    day = forms.IntegerField(
        label='납부일(매월)',
        min_value=1,
        max_value=31,
        widget=forms.NumberInput(attrs={'placeholder': '1~31'}),
    )
        
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