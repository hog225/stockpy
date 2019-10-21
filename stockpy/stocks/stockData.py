import pandas as pd
import requests
from io import BytesIO
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import time
import talib as TA
import numpy as np
import math
from dateutil import relativedelta

# 하강 패턴
BEARISH_ENGULFING = 'BE_CDLENGULFING'
DARK_CLOUD_COVER = 'CDLDARKCLOUDCOVER'
EVENING_STAR = 'CDLEVENINGSTAR' # 주가 상방에서 하락 반전 신호로 인식됨
GRAVESTONE_DOJI = 'CDLGRAVESTONEDOJI' ## 주가 상방에서 하락 반전 신호로 인식됨
HANGING_MAN = 'CDLHANGINGMAN' # 주가 상승추세 꼭대기에서 하락 반전 신호로 인식
SHOOTING_STAR = 'CDLSHOOTINGSTAR' # 주가 상방에서 하락 반전 신호로 인식됨
TWEEZERTOP = 'NotExist'
# --------------------------------------------------

# 상승 패턴
BULLISH_ENGULFING = 'BU_CDLENGULFING'
DRAGONFLY_DOJI = 'CDLDRAGONFLYDOJI' # 주가 하방에서 상승 반전 신호로 인식됨
HAMMER = 'CDLHAMMER' # 하양추세 바닥에서 상승신호
INVERTED_HAMMER = 'CDLINVERTEDHAMMER' # 하양추세 바닥에서 상승으로 갈 수 있다는 경고 다른 패턴 보다 신뢰성 떨어짐
MORNING_STAR = 'CDLMORNINGSTAR' # 하양추세 바닥에서 상승신호
PIERCING_PATTERN = 'CDLPIERCING'  # 상승신호 BULLISH_ENGULFING 이랑 비슷
TWEEZERBOTTOM = 'NotExist'
# --------------------------------------------------

# 추세 변경 신호
DOJI = 'CDLDOJI'
HARAMI = 'CDLHARAMI'
# --------------------------------------------------

# MOMENTUM INDICATOR
JONBER = 1
ADX = 2 # Average Directional Movement Index 방향이동 지표를 보조하는 수단 +DI -DI 뚫고 올라가면 매수 신호 반대의 경우 매도 신호
APO = 3 # Absolute Price Oscillator 두 지수 이동 평균의 차를 표시함 0 위로 뚫고 올라가면 매수 신호 반대의 경우 매도 신호
AROONOSC = 4 # Aroon Oscillator 오실레이터가 0을 뚫고 올라가면 상승 트렌드 시작 반대면 하강 트렌드
CCI = 5 # Commodity channel index Donald Lambert 과매수 과매도를 판단하기 위해 사용됨 70 ~80 들갔다가 내려오면 매도 , 20 ~30 들갔다가 올라올때 매수
MA = 6
MACD = 7
RSI = 8
STOCH = 9

BUY = 2.0
SELL = -2.0

def checkTime(func):
    def decorator(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print('FUNC : ', func.__name__, ' Precess Time : ', time.time()-start)
        return result
    return decorator

def getStockDataBasic():
    markets = [{'kospi': 'stockMkt'}, {'kosdaq': 'kosdaqMkt'}]
    for market in markets:

        market_name = [*market][0]
        # try:
        #     m_obj = Market.objects.get(market_name=market_name)
        # except Market.DoesNotExist:
        #     m_obj = Market(market_name=market_name)
        #     m_obj.save()

        url_market = market[market_name]
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=%s' % url_market
        df = pd.read_html(url, header=0)[0]

        df_nameAndCode = df[['회사명', '종목코드']]
        df_nameAndCode['종목코드'] = df_nameAndCode['종목코드'].astype(str)
        df_nameAndCode['종목코드'] = df_nameAndCode['종목코드'].str.zfill(6)

        for idx, namecode in df_nameAndCode.iterrows():
            stockName = namecode['회사명']
            stockCode = namecode['종목코드']

            # try:
            #     obj = Stock.objects.get(stock_name=stockName)
            #     Stock.objects.filter(stock_name=stockName).update(stock_code=stockCode, f_market=m_obj)
            # except Stock.DoesNotExist:
            #     obj = Stock(stock_name=stockName, stock_code=stockCode, f_market=m_obj)
            #     obj.save()
    pass

def getStockMarket():
    markets = [{'kospi': 'STK'}, {'kosdaq': 'KSQ'}]
    return markets

# https://blog.naver.com/flow2kudo/221319347186 인용
@checkTime
def getStockDataFromKrxMktData(q_mkt_name):
    gen_req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
    query_str_parms = {
        'name': 'fileDown',
        'filetype': 'xls',
        'url': 'MKD/04/0406/04060100/mkd04060100_01',
        'market_gubun': q_mkt_name,
        'isu_cdnm': '전체',
        'sort_type': 'A',
        'lst_stk_vl': '1',
        'pagePath': '/contents/MKD/04/0406/04060100/MKD04060100.jsp'
    }

    r = requests.get(gen_req_url, query_str_parms)

    gen_req_url = 'http://file.krx.co.kr/download.jspx'
    headers = {
        'Referer': 'http://marketdata.krx.co.kr/mdi'
    }
    form_data = {
        'code': r.content
    }
    r = requests.post(gen_req_url, form_data, headers=headers)
    df = pd.read_excel(BytesIO(r.content))

    df_stockData = df[['기업명', '종목코드', '업종코드', '상장주식수(주)', '자본금(원)']]
    df_stockData['종목코드'] = df_stockData['종목코드'].astype(str)
    df_stockData['종목코드'] = df_stockData['종목코드'].str.zfill(6)

    df_stockData['업종코드'] = df_stockData['업종코드'].astype(str)
    df_stockData['업종코드'] = df_stockData['업종코드'].str.zfill(6)

    df_stockData['최초상장일'] = None
    for idx, data in df_stockData.iterrows():
        vf_listed_date = getVeryFirstListDateFromNaver(data['종목코드'])
        data['최초상장일'] = vf_listed_date


    return df_stockData

# kospi 개장 1980 년 14531
def getVeryFirstListDateFromNaver(stock_code):
    url = 'https://fchart.stock.naver.com/sise.nhn?symbol=%s&timeframe=day&startTime=20021101&count=1&requestType=0' % stock_code
    r = requests.get(url)
    root = ET.fromstring(r.text)

    chartData = root.find("./chartdata").attrib
    vf_listed_date = datetime.datetime.strptime(chartData['origintime'], "%Y%m%d").date()
    return vf_listed_date

def getStockValueFromNaver(stock_code, reqtype, count= 14531, date=None):
    url = 'https://fchart.stock.naver.com/sise.nhn?symbol=%s&timeframe=day&startTime=20021101&count=%d&requestType=%d' % (stock_code, count, reqtype)
    r = requests.get(url)
    root = ET.fromstring(r.text)

    df_org = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume'])
    for data in root.findall("./chartdata/item"):
        stockVal = data.attrib['data'].split('|')
        stockVal[0] = datetime.datetime.strptime(stockVal[0], "%Y%m%d").date()
        stockVal.append(None)

        df_new = pd.DataFrame([stockVal], columns=['Date', 'Open', 'High', 'Low','AdjClose', 'Volume', 'Close'])
        df_org = df_org.append(df_new, ignore_index=True, sort= False)

    return df_org

def getTradePointFromMomentum(tech_anal_code, df_stock_val):
    buyList = []
    sellList = []


    df_stock_val['trade'] = 0
    if tech_anal_code == JONBER:
        df_stock_val.loc[df_stock_val.index[0], 'trade'] = BUY
        df_stock_val.loc[df_stock_val.index[-1], 'trade'] = SELL

    if tech_anal_code == MACD:
        se_macd, se_macdsignal, se_macdhist = TA.MACD(df_stock_val.AdjClose, fastperiod=12, slowperiod=26, signalperiod=9)
        se_signal = np.sign(se_macd - se_macdsignal)
        se_signal = se_signal - se_signal.shift()
        se_signal[np.isnan(se_signal)] = 0.0
        df_stock_val['trade'] = se_signal
        # -2.0 DeadCross 2.0 GoldCross SELL, BUY

    print('Trade List : ')
    print(df_stock_val['trade'][df_stock_val['trade'] != 0.0])
    return df_stock_val

# 다음 에 해야함 패턴 인식을 통한 매매
def getTradePointFromPatternRecorg(pattern_name, df):
    pass

def makeResultData(df_stock_val, balance):
    pass
    buyList = []
    sellList = []



    se_trade = df_stock_val['trade'][df_stock_val['trade'] != 0.0]
    if len(se_trade[se_trade == 2].index) == 0:
        return buyList, sellList, pd.Series(), pd.Series(), pd.Series()
    first_buy_idx = se_trade[se_trade == 2].index[0]

    df_stock_val['Balance'] = 0.0
    df_stock_val['Asset'] = 0.0
    df_stock_val['StockCount'] = 0.0

    if first_buy_idx == 0:
        df_stock_val.loc[0, ['Balance', 'Asset', 'StockCount']] = balance, balance, 0
    else:
        df_stock_val.loc[0:first_buy_idx , ['Balance', 'Asset', 'StockCount']] = balance, balance, 0

    beforeIdx = first_buy_idx
    #for idx, value in se_trade.loc[first_buy_idx:].items():
    se_idx_list = se_trade.loc[first_buy_idx:].index
    for idx, realIdx in enumerate(se_idx_list):

        if idx == 0 or \
                se_trade.loc[realIdx] == BUY and \
                se_trade.loc[beforeIdx] != se_trade.loc[realIdx]:

            stock_count = math.floor(balance / df_stock_val.loc[realIdx].AdjClose)
            balance -= stock_count * df_stock_val.loc[realIdx].AdjClose

            if idx == len(se_idx_list) - 1:
                df_stock_val.loc[realIdx: , ['Balance', 'Asset', 'StockCount']] = \
                    balance, balance + (df_stock_val.loc[realIdx:]['AdjClose']* stock_count), stock_count
            else:
                df_stock_val.loc[realIdx:se_idx_list[idx + 1], ['Balance', 'Asset', 'StockCount']] = \
                    balance, balance + (df_stock_val.loc[realIdx:se_idx_list[idx + 1]]['AdjClose'] * stock_count), stock_count

            buyList.append([
                df_stock_val.loc[realIdx].Date.strftime("%Y-%m-%d"),
                df_stock_val.loc[realIdx].AdjClose
            ])

            beforeIdx = realIdx


        elif se_trade.loc[realIdx] == SELL and \
                se_trade.loc[beforeIdx] != se_trade.loc[realIdx]:
            stock_count = df_stock_val.loc[realIdx]['StockCount']
            balance += stock_count * df_stock_val.loc[realIdx].AdjClose
            asset = balance
            stock_count = 0

            if idx == len(se_idx_list) - 1:
                df_stock_val.loc[realIdx:, ['Balance', 'Asset', 'StockCount']] = \
                    balance, asset, stock_count
            else:
                df_stock_val.loc[realIdx:se_idx_list[idx + 1], ['Balance', 'Asset', 'StockCount']] = \
                    balance, asset, stock_count

            sellList.append([
                df_stock_val.loc[realIdx].Date.strftime("%Y-%m-%d"),
                df_stock_val.loc[realIdx].AdjClose
            ])

            beforeIdx = realIdx


    # 매매 시점에 따라서 Balance 데이터를 변경 시킴 필요 데이터 Balance(현금), Asset(현금 + 주식가치), Stock Count

    # 1, BUY 시점을 찾아서 매수를 때리고 (이때 Buy 리스트 추가 )
    # Stocks 에 산수량 Blance엔 산 수량만큼 차감 이 수치를 다음 Sell Point -1 까지 적용 그리고 Asset 에는 Stock count * 그시점 종가
    # 2, 이 후 Sell Point 시 Stocks 를 0으로 만들고 Blace에 ADD Asset = Balance 다음 Buy point -1 까지 적용
    # 3, 1 ~ 2 번 반복

    # 아래 데이터 pd 시리즈 예상
    print(df_stock_val)
    return buyList, sellList, df_stock_val['Balance'], df_stock_val['Asset'], df_stock_val['StockCount']


def makeResultText(df_stock_val):

    org_asset = df_stock_val.iloc[0].Asset
    last_asset = df_stock_val.iloc[-1].Asset
    final_yield = 100 * ((last_asset - org_asset) / org_asset)
    r = relativedelta.relativedelta(df_stock_val.iloc[-1].Date, df_stock_val.iloc[0].Date)
    if r.years:
        period_str = '%d 년 %d달 %d일' % (r.years, r.months, r.days)
    elif r.months:
        period_str = '%d달 %d일' % (r.months, r.days)
    elif r.days:
        period_str = '%d일' % (r.days)


    text = '원금 %s원은 투자기간 %s 이후 %s원이 되었습니다. \n' % ('{:,}'.format(int(org_asset)), period_str, '{:,}'.format(int(last_asset)))
    text += '원금 대비 번 돈은 %s원이며 수익률은 %.2f%% 입니다. \n' % ('{:,}'.format(int(last_asset - org_asset)), final_yield)
    #text += '초기 주식 보유량은 %d 이고 마지막 보유량은 %d 입니다. \n'
    #text += '투자 성과가 가장 좋았던 해는 %년 처음 자산 %s 에서 마지막 자산 %s 로 증가 했습니다. \n'
    # http://www.index.go.kr/potal/stts/idxMain/selectPoSttsIdxSearch.do?idx_cd=1073 / 역대 금리 리스트
    #text += '원금 %s를 같은 기간동안 은행에 맡겼으면 기준금리 기준 %s원이 되었을 겁니다.'
    #text += '종합적으로 당신의 투자는 %s 했습니다. \n'
    return text



if __name__ == "__main__":

    print(getStockValueFromNaver('034730', 0, count=10))

    #print(getVeryFirstListDateFromNaver('005930'))
    #df_stockData = getStockDataFromKrxMktData('KSQ')
    #print(df_stockData)





