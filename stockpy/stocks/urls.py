from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('if-i-bought/init-stocks', views.initStockData, name='initStockData'),
    path('if-i-bought/update-market', views.updateMarket, name='updateMarket'),
    path('if-i-bought/update-stock-value', views.updateStockValue, name='updateStockValue'),
    path('if-i-bought/', views.if_i_bought_main, name='if_i_bought_main'),
    url(r'^stock-name-autocomplete/$', views.StocksAutocomplete, name='stock-name-autocomplete'),
    url(r'^marketSelectAjax/$', views.marketSelectAjax, name='marketSelectAjax'),

]