from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('if-i-bought/', views.if_i_bought_main, name='if_i_bought_main'),
]