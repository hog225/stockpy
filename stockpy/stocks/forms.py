from .models import *


class StockInfoSelectForm(forms.Form):
    market_name = forms.ModelChoiceField(queryset=Market.objects.all(), label='Market')

    if TechAnal.objects.all().count() > 0:
        tech_anal_name = forms.ModelChoiceField(queryset=TechAnal.objects.all(), label='Technical analysis', required=False, initial=1)
    else:
        tech_anal_name = forms.ModelChoiceField(queryset=TechAnal.objects.all(), label='Technical analysis', required=False)

    stock_name = forms.CharField(max_length=50, label='Stocks', widget=forms.TextInput(
        attrs={
            #'style': 'width: 400px',
            'class': 'stockNameAutoComplete',
            'disabled': 'disabled',
            #'data-url': "/domain/stock_name_autocomplete/"
        }
    ))





