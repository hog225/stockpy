from .models import *
import datetime
import re
from django.template.defaultfilters import mark_safe

class techAnalWidget(forms.Select):
    def __init__(self, *args, **kwargs):
        # attribute for select
        cus_attrs = {
            'name': "opts"
            # 'data-toggle': "tooltip",
            # 'data-placement': "bottom",

        }
        super().__init__(cus_attrs, *args, **kwargs)

    def create_option(self, name, value, *args, **kwargs):
        option = super().create_option(name, value, *args, **kwargs)
        if value:
            tech_anal = self.choices.queryset.get(pk=value)
            option['attrs']['title'] = tech_anal.comment  # set option attribute
            option['attrs']['data-toggle'] = "tooltip"  # set option attribute
            option['attrs']['data-placement'] = "right"  # set option attribute

        return option

class StockInfoSelectForm(forms.Form):
    market_name = forms.ModelChoiceField(queryset=Market.objects.all(), label=mark_safe('<strong>Market</strong>'))

    # try 안하면 초기 Django Model 생성시 에러 발생
    try:
        if TechAnal.objects.all().count() > 0:
            tech_anal_name = forms.ModelChoiceField(queryset=TechAnal.objects.all(), label=mark_safe('<strong>Technical analysis</strong>'),
                                                    required=False, initial=1, widget=techAnalWidget)
        else:
            tech_anal_name = forms.ModelChoiceField(queryset=TechAnal.objects.all(), label=mark_safe('<strong>Technical analysis</strong>'), required=False)
    except:
        pass

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

        if (self.cleaned_data['end_date'].date() - self.cleaned_data['start_date'].date()).days < 1:
            return False, '투자 종료일이 시작일과 얼마 차이 나지 않거나 빠릅니다.'

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






