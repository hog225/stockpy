from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
#from .models import MarketForm, TechAnalForm, StockNameForm
from .forms import StockInfoSelectForm
from .models import Stock
from dal import autocomplete

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

class StocksAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #     return Stock.objects.none()

        qs = Stock.objects.all()

        if self.q:
            qs = qs.filter(stock_name__startswith=self.q)
            #qs = qs.filter(stock_name__istartswith=self.q).values()

        return qs