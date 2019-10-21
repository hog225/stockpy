from .models import *
import datetime
import re
from django.template.defaultfilters import mark_safe

class StockInfoSelectForm(forms.Form):
    market_name = forms.ModelChoiceField(queryset=Market.objects.all(), label=mark_safe('<strong>Market</strong>'))

    if TechAnal.objects.all().count() > 0:
        tech_anal_name = forms.ModelChoiceField(queryset=TechAnal.objects.all(), label=mark_safe('<strong>Technical analysis</strong>'), required=False, initial=1)
    else:
        tech_anal_name = forms.ModelChoiceField(queryset=TechAnal.objects.all(), label=mark_safe('<strong>Technical analysis</strong>'), required=False)

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

    stock_name = forms.CharField(max_length=50, label=mark_safe('<strong>Stocks</strong>'), widget=forms.TextInput(
        attrs={
            #'style': 'width: 400px',
            'class': 'stockNameAutoComplete',
            'disabled': 'disabled',
            #'data-url': "/domain/stock_name_autocomplete/"
        }
    ))

    investment_amount = forms.CharField(label=mark_safe('<strong>투자금액(원)</strong>'), widget=forms.TextInput(
        attrs={
            'type': 'money',
        }

    ))

    def is_valid(self):
        valid = super(StockInfoSelectForm, self).is_valid()

        if not valid:
            return valid, 'form error'

        try:
            obj_market = Market.objects.get(market_name = self.cleaned_data['market_name'])
        except Market.DoesNotExist:
            return False, 'Not Exist Market Name'

        try:
            TechAnal.objects.get(tech_anal_name = self.cleaned_data['tech_anal_name'])
        except Market.DoesNotExist:
            return True, 'Not Exist Tech Anal'

        try:
            if self.cleaned_data['start_date'].date() - datetime.datetime.now().date() > datetime.timedelta(0):
                return False, 'Invalid Start Date'
        except Exception as e:
            print(e)
            return False, 'Invalid Date Format'

        try:
            if self.cleaned_data['end_date'].date() - datetime.datetime.now().date() > datetime.timedelta(0):
                return False, 'Invalid End Date'
        except Exception as e:
            print(e)
            return False, 'Invalid Date Format'

        try:
            money = re.sub("[^\d\.]", "", self.cleaned_data['investment_amount'])

            if len(money) > 13: # 조단위
                return False, 'Too Much Money'
        except:
            return False, 'Invalid Money'

        try:
            Stock.objects.get(stock_name = self.cleaned_data['stock_name'], f_market = obj_market)
        except Stock.DoesNotExist:
            return False, 'Not Exist Stock'




        return True, 'Success'






