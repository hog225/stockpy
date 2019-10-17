from .models import *
import datetime


class StockInfoSelectForm(forms.Form):
    market_name = forms.ModelChoiceField(queryset=Market.objects.all(), label='Market')

    if TechAnal.objects.all().count() > 0:
        tech_anal_name = forms.ModelChoiceField(queryset=TechAnal.objects.all(), label='Technical analysis', required=False, initial=1)
    else:
        tech_anal_name = forms.ModelChoiceField(queryset=TechAnal.objects.all(), label='Technical analysis', required=False)

    start_date = forms.DateTimeField(
        input_formats=['%Y/%m/%d'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

    end_date = forms.DateTimeField(
        input_formats=['%Y/%m/%d'],
        initial= datetime.datetime.now().strftime("%Y/%m/%d"),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
        })
    )

    stock_name = forms.CharField(max_length=50, label='Stocks', widget=forms.TextInput(
        attrs={
            #'style': 'width: 400px',
            'class': 'stockNameAutoComplete',
            'disabled': 'disabled',
            #'data-url': "/domain/stock_name_autocomplete/"
        }
    ))

    investment_amount = forms.CharField(label='투자금액(원)', widget=forms.TextInput(
        attrs={
            'type': 'money',
        }

    ))





