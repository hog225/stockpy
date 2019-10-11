from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import StockInfoSelectForm
from .models import Stock, Market
from django.contrib.auth.decorators import login_required
#from dal import autocomplete
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd

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

@login_required
def getStockCode(request):
    if request.method == "POST":
        markets = [{'kospi':'stockMkt'}, {'kosdaq':'kosdaqMkt'}]
        for market in markets:

            market_name = [*market][0]
            try:
                m_obj = Market.objects.get(market_name = market_name)
            except Market.DoesNotExist:
                m_obj = Market(market_name = market_name)
                m_obj.save()

            url_market = market[market_name]
            url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=%s' % url_market
            df = pd.read_html(url, header=0)[0]

            df_nameAndCode = df[['회사명', '종목코드']]
            df_nameAndCode['종목코드'] = df_nameAndCode['종목코드'].astype(str)
            df_nameAndCode['종목코드'] = df_nameAndCode['종목코드'].str.zfill(6)

            for idx, namecode in df_nameAndCode.iterrows():
                stockName = namecode['회사명']
                stockCode = namecode['종목코드']

                try:
                    obj = Stock.objects.get(stock_name=stockName)
                    Stock.objects.filter(stock_name=stockName).update(stock_code=stockCode, f_market=m_obj)
                except Stock.DoesNotExist:
                    obj = Stock(stock_name=stockName, stock_code=stockCode, f_market=m_obj)
                    obj.save()

        return redirect('/stocks/if_i_bought')

    return redirect('/stocks/index')



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

#@csrf_exempt
def marketSelectAjax(request):

    if request.POST.__contains__('selectedVal'):
        data = request.POST['selectedVal']
        market_name_str = Market.objects.get(id=data).market_name
        context = {'selectedVal': market_name_str, }
        print('Selected Val is ', market_name_str)

        json_data = json.dumps(context)

        return HttpResponse(json_data, 'application/json')
    return HttpResponse(status=404)