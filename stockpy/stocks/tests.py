from django.test import TestCase

# Create your tests here.

import pandas as pd
from stocks.models import Stock, Market, StockValue
from stocks.stockData import *
from stocks.views import *

stock_obj = Stock.objects.get(stock_code='005930')
sv_objs = StockValue.objects.filter(f_stock_id=stock_obj).order_by('date')

a = StockInfoSelectForm({
    "market_name":1,
    "tech_anal_name":1,
    "stock_name": "CJ CGV",
    "start_date": "2019/09/30",
    "end_date": "2019/10/19",
    "investment_amount":"234"
})