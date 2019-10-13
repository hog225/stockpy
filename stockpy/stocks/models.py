from django.db import models
from django.forms import ModelForm
from django import forms

# Create your models here.


class Market(models.Model):
    market_name = models.CharField(max_length=25)
    pub_date = models.DateTimeField('date published', auto_now_add=True, null=True)
    update_date = models.DateTimeField('data updated', auto_now=True, null=True)

    def __str__(self):
        return self.market_name

class TechAnal(models.Model):
    tech_anal_name = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published', auto_now_add=True, null=True)
    update_date = models.DateTimeField('data updated', auto_now=True, null=True)

    def __str__(self):
        return self.tech_anal_name

class Stock(models.Model):
    stock_name = models.CharField(max_length=50)
    stock_code = models.CharField(max_length=10)
    f_market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='stock')
    business_type_code = models.CharField(max_length=10, null=True)
    listed_shares = models.CharField(max_length=30, null=True)
    capital = models.CharField(max_length=30, null=True)
    vf_listed_date = models.DateField('very first listed date', null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True, null=True)
    update_date = models.DateTimeField('data updated', auto_now=True, null=True)

    def __str__(self):
        return self.stock_name

class StockValue(models.Model):
    f_stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stockvalue', null=True)
    high = models.FloatField(null=True)
    low = models.FloatField(null=True)
    close = models.FloatField(null=True)
    open = models.FloatField(null=True)
    adj_close = models.FloatField(null=True)
    volume = models.IntegerField(null=True)
    date = models.DateField(null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True, null=True)
    update_date = models.DateTimeField('data updated', auto_now=True, null=True)


