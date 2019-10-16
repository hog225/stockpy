from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import StockInfoSelectForm
from .models import Stock, Market, StockValue
from django.contrib.auth.decorators import login_required
#from dal import autocomplete
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from .stockData import *
import datetime
from django.template import loader

def index(request):
    template = loader.get_template('stocks/index.html')
    return HttpResponse(template.render({}, request))

def if_i_bought_main(request):
    if request.method == "POST":
        form = StockInfoSelectForm(request.POST)

        if form.is_valid():

            print(form.cleaned_data)

        return redirect('/stocks/index')
    else:
        form = StockInfoSelectForm()
        return render(request, 'stocks/if_i_bought_main.html', {'form' : form})

@checkTime
def saveStockValue(stock_obj, last_date_on_db=None):
    # stock_obj = Stock.objects.get(stock_name='CJ')
    print('Save stock value :', stock_obj.stock_name)
    if last_date_on_db != None:
        td = datetime.date.today() - last_date_on_db
        df_tmp_stock = getStockValueFromNaver(stock_obj.stock_code, 0, count=td.days+1)
        df_stock = df_tmp_stock[df_tmp_stock.Date > last_date_on_db]
    else:
        df_stock = getStockValueFromNaver(stock_obj.stock_code, 0)
    sv_obj = []

    start = time.time()
    obj = StockValue.objects.filter(f_stock=stock_obj)
    for idx, stock_dat in df_stock.iterrows():
        if obj:
            try:
                tmp_obj = obj.get(date=stock_dat['Date'])
            except StockValue.DoesNotExist:
                tmp_obj = StockValue(
                    f_stock=stock_obj,
                    date=stock_dat['Date'],
                    high=stock_dat['High'],
                    low=stock_dat['Low'],
                    close=stock_dat['Close'],
                    open=stock_dat['Open'],
                    adj_close=stock_dat['AdjClose'],
                    volume=stock_dat['Volume']
                )
                sv_obj.append(tmp_obj)
        else:
            tmp_obj = StockValue(
                f_stock=stock_obj,
                date=stock_dat['Date'],
                high=stock_dat['High'],
                low=stock_dat['Low'],
                close=stock_dat['Close'],
                open=stock_dat['Open'],
                adj_close=stock_dat['AdjClose'],
                volume=stock_dat['Volume']
            )
            sv_obj.append(tmp_obj)

    StockValue.objects.bulk_create(sv_obj)

@login_required
def initStockData(request):
    if request.method == "POST":
        # 시장 데이터 저장
        markets = getStockMarket()
        for market in markets:
            market_name = [*market][0]
            try:
                m_obj = Market.objects.get(market_name = market_name)
            except Market.DoesNotExist:
                m_obj = Market(market_name = market_name)
                m_obj.save()

        # 시장별 주식 종목 정보 데이터 저장
        print('Save Market Data')
        for market in markets:
            market_name = [*market][0]
            q_mkt_name = market[market_name]
            df_stockData = getStockDataFromKrxMktData(q_mkt_name)
            try:
                m_obj = Market.objects.get(market_name=market_name)
            except Market.DoesNotExist:
                return HttpResponse("ERROR")

            for idx, namecode in df_stockData.iterrows():
                stockName = namecode['기업명']
                stockCode = namecode['종목코드']
                stockBussinesCode = namecode['업종코드']
                stockListedShares = namecode['상장주식수(주)']
                stockCapital = namecode['자본금(원)']
                stockVFDate = namecode['최초상장일']

                try:
                    obj = Stock.objects.get(stock_code=stockCode)
                    if stockVFDate == None:
                        continue

                    Stock.objects.filter(stock_code=stockCode).update(
                        stock_name=stockName,
                        f_market=m_obj,
                        business_type_code=stockBussinesCode,
                        capital=stockCapital,
                        listed_shares=stockListedShares,
                        vf_listed_date=stockVFDate
                    )
                except Stock.DoesNotExist:
                    obj = Stock(
                        stock_name=stockName,
                        stock_code=stockCode,
                        f_market=m_obj,
                        business_type_code=stockBussinesCode,
                        capital=stockCapital,
                        listed_shares=stockListedShares,
                        vf_listed_date=stockVFDate
                    )
                    obj.save()

        print('Save Stock Value Start ')
        for stock_obj in Stock.objects.all():
            saveStockValue(stock_obj)


        return redirect('/stocks/if-i-bought')



    return redirect('/stocks/index')

@login_required
def updateMarket(request):
    # 마켓데이터 그리고 마켓에 속한 종목을 업데이트 한다.
    # 새로 추가된 마켓이 있으면 종목을 업데이트 하고 종목의 자산 가격을 업데이트 한다.
    # 상패가 되었으면 DB 추가 해서 상패라고 써논다.
    # 액면 분할이 나 어떤 ADJClose의 영향을 줄 경우 StockValue를 업데이트 한다.
    # 기존 리스트 대비 새로 상장 되었으면 주가 데이터를 추가 한다.
    #


    return redirect('/stocks/index')


@login_required
def updateStockValue(request):
    # 주가, 자산가격을 업데이트 한다.
    # 현제 DB의 가장 마지막 Date를 알아낸뒤
    for stock_obj in Stock.objects.all():
        recentDate = StockValue.objects.filter(f_stock_id=stock_obj).order_by('-date')[0].date
        if datetime.date.today() - recentDate >= datetime.timedelta(days=1) and datetime.datetime.today().hour > 20:
            saveStockValue(stock_obj, recentDate)

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