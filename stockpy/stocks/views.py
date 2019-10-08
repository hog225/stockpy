from django.shortcuts import render, redirect
from django.http import HttpResponse
#from .models import MarketForm, TechAnalForm, StockNameForm
from .forms import StockInfoSelectForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def if_i_bought_main(request):
    if request.method == "POST":
        form = StockInfoSelectForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data['market_name'])
        return redirect('/stocks/index')
    else:
        form = StockInfoSelectForm()
        return render(request, 'stocks/if_i_bought_main.html', {'form' : form})

