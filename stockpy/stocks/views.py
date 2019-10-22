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
import re

def convertORMtoStockValueDataFrame(orm_obj):
    df_org = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume'])
    df_org['Date'] = list(orm_obj.values_list('date', flat=True))
    df_org['Open'] = list(orm_obj.values_list('open', flat=True))
    df_org['High'] = list(orm_obj.values_list('high', flat=True))
    df_org['Low'] = list(orm_obj.values_list('low', flat=True))
    df_org['Close'] = list(orm_obj.values_list('close', flat=True))
    df_org['AdjClose'] = list(orm_obj.values_list('adj_close', flat=True))
    df_org['Volume'] = list(orm_obj.values_list('volume', flat=True))

    return df_org

def index(request):
    template = loader.get_template('stocks/index.html')
    return HttpResponse(template.render({}, request))

def if_i_bought_main(request):
    if request.method == "POST":
        code = 200
        form = StockInfoSelectForm(request.POST)
        result, cause = form.is_valid()
        print(cause)
        if result:

            stock_obj = Stock.objects.get(stock_name = form.cleaned_data['stock_name'])
            # 아래 from, to 지정 필요 !!!!!!!!!!
            sv_objs = StockValue.objects.filter(f_stock_id=stock_obj).order_by('date')
            s_date = form.cleaned_data['start_date'].date()
            e_date = form.cleaned_data['end_date'].date()
            sv_objs = sv_objs.filter(date__range=(s_date, e_date))

            if len(sv_objs) < 2:
                resStr = "최소한 2 비지니스 데이 이상의 기간을 입력해 주세요"
                jsonData = json.dumps({'result': resStr})
                code = 400
                mimetype = 'application/json'
                return HttpResponse(jsonData, mimetype, status=code)
            # s_date = sv_objs[0].date
            # e_date = sv_objs[len(sv_objs)-1].date

            valueList = []
            for obj in sv_objs:

                valueList.append([
                    obj.date.strftime("%Y-%m-%d"),
                    #datetime.datetime.timestamp(datetime.datetime.fromordinal(obj.date.toordinal())),
                    obj.adj_close
                ])




            balance = int(re.sub("[^\d\.]", "", form.cleaned_data['investment_amount']))
            if balance < sv_objs[0].adj_close:
                resStr = "입력한 투자금액으로는 한 주도 살 수 없습니다. %s원 이상으로 입력해주세요!" % '{:,}'.format(int(sv_objs[0].adj_close))
                jsonData = json.dumps({'result': resStr})
                code = 400
                mimetype = 'application/json'
                return HttpResponse(jsonData, mimetype, status=code)

            df_stock_val = convertORMtoStockValueDataFrame(sv_objs)

            res, overlayChartSet, overlayNameList = makeOverlayChartData(df_stock_val, MA, {'ma_5': 5, 'ma_10': 10, 'ma_25': 25})

            # 아래 함수 makeResultData 로 대체 되어야함
            df_stock_val = getTradePointFromMomentum(form.cleaned_data['tech_anal_name'].code, df_stock_val)
            b_list, s_list, se_balance, se_asset, se_stock_count = makeResultData(df_stock_val, balance)
            if b_list == []:
                resStr = "요청한 기술적 분석으로 거래가 이루어지지 않았습니다. 기간을 변경해 보시거나 기술적 분석 전략을 변경해 보세요!"
                jsonData = json.dumps({'result': resStr})
                code = 400
                mimetype = 'application/json'
                return HttpResponse(jsonData, mimetype, status=code)

            org_asset = df_stock_val.iloc[0].Asset
            last_asset = df_stock_val.iloc[-1].Asset
            added_asset = last_asset - org_asset
            final_yield = 100 * (added_asset / org_asset)
            str_invest_period = getInvestPeriod(df_stock_val.iloc[0].Date, df_stock_val.iloc[-1].Date)

            jsonData = json.dumps({
                'result': 'Success',
                'data': valueList,
                'stockName': form.cleaned_data['stock_name'],
                'buyList' : b_list,
                'sellList' : s_list,
                'orgAsset' : '{:,}'.format(int(org_asset)),
                'lastAsset': '{:,}'.format(int(last_asset)),
                'addedAsset': '{:,}'.format(int(added_asset)),
                'final_yield': '%.2f%%' % final_yield,
                'period': str_invest_period,
                'overlayNameList': overlayNameList,
                'overlayChartList': overlayChartSet
            })


        else:
            jsonData = json.dumps({'result': cause})
            code = 400


        mimetype = 'application/json'
        return HttpResponse(jsonData, mimetype, status=code)


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
        if datetime.date.today() - recentDate >= datetime.timedelta(days=1):
            saveStockValue(stock_obj, recentDate)

    return redirect('/stocks/index')

# django-autocomplete-light 사용 하려다가 포기함
def StocksAutocomplete(request):
    if request.GET.__contains__('q'):

        try:
            market_key = request.GET['s']
            obj_market = Market.objects.get(id=market_key)
            qs = Stock.objects.filter(stock_name__startswith=request.GET['q'], f_market=obj_market)
        except Exception as e:
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