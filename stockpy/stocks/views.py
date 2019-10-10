from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import StockInfoSelectForm
from .models import Stock
#from dal import autocomplete
import json

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

# django-autocomplete-light 사용 하려다가 포기함
def StocksAutocomplete(request):
    if request.GET.__contains__('q'):
        qs = Stock.objects.filter(stock_name__startswith=request.GET['q'])
        results = []
        for q in qs:
            tag_json = {}
            tag_json['id'] = q.id
            tag_json['label'] = q.stock_name
            tag_json['value'] = q.stock_name
            results.append(tag_json)
        data = json.dumps(results)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    return HttpResponse()

