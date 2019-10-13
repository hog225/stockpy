import pandas as pd
import requests
from io import BytesIO
import urllib.parse
import xml.etree.ElementTree as ET
import datetime


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



if __name__ == "__main__":

    print(getStockValueFromNaver('034730', 0, count=10))

    #print(getVeryFirstListDateFromNaver('005930'))
    #df_stockData = getStockDataFromKrxMktData('KSQ')
    #print(df_stockData)





