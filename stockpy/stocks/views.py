from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MarketForm, TechAnalForm

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def if_i_bought_main(request):
    if request.method == "POST":
        m_form = MarketForm(request.POST)
        t_form = TechAnalForm(request.POST)
        if m_form.is_valid() or t_form.is_valid():
            print(m_form.cleaned_data['market_name'])

        return redirect('/stocks/index')
    else:
        m_form = MarketForm()
        t_form = TechAnalForm()

        return render(request, 'stocks/if_i_bought_main.html', {'m_form': m_form, 't_form': t_form})

