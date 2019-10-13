from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('if-i-bought/init-stocks', views.updateStockCode, name='updateStockCode'),
    path('if-i-bought/', views.if_i_bought_main, name='if_i_bought_main'),
    url(r'^stock-name-autocomplete/$', views.StocksAutocomplete, name='stock-name-autocomplete'),
    url(r'^marketSelectAjax/$', views.marketSelectAjax, name='marketSelectAjax'),

]