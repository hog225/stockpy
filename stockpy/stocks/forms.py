from .models import *
from dal import autocomplete

class StockInfoSelectForm(forms.Form):
    market_name = forms.ModelChoiceField(queryset=Market.objects.all(), label='Market')
    tech_anal_name = forms.ModelChoiceField(queryset=TechAnal.objects.all(), label='Technical analysis')
    stock_name = forms.CharField(max_length=50, label='Stocks', widget=forms.TextInput(
        attrs={
            #'style': 'width: 400px',
            'class': 'basicAutoComplete',
            #'data-url': "/domain/stock_name_autocomplete/"
        }
    ))





