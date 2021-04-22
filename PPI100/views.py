from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
import requests
import re
import xml.etree.ElementTree as ET
import pandas as pd
import json

from datetime import datetime
from .scraper import test
from .scraper import Scraped_100PPI_Data
from .models import mst_PPI100
from django.contrib import messages

# Create your views here.
def index(request):

    if request.method == 'POST' and 'refresh' in request.POST:
        # import ipdb; ipdb.set_trace()
        Scraped_100PPI_Data()
        messages.success(request, 'data has been fetched successfully till latest date')


    context=getComname()
    return render(request,'index.html',context)

def scraper(request):

    context=getComname()

    if request.method=="POST":
        entries= mst_PPI100.objects.all()
        # entries.delete()     #delete entire data from table
        Scraped_100PPI_Data()


    return render(request,'scraper.html',context)

def getComname():

    df = pd.DataFrame(list(mst_PPI100.objects.values_list('Commodity')),columns =['commodity'])
    df=df.drop_duplicates(subset=None, keep='first', inplace=False)
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
    return context

def result(request):

    if request.method=="POST":
        sdate=request.POST.get("sdate")
        edate=request.POST.get("edate")
        product_name=request.POST.get("product_name")
        
        context=getComdata(product_name,sdate,edate)

    if context=="empty":

        return render(request,'noresult.html')
        # messages.success(request, 'No results found for selected dates')
    else:
        return render(request,'result.html',context)


def getComdata(product_name,sdate,edate):

    sdate=date_time_obj = datetime.strptime(sdate, '%Y-%m-%d')
    # sdate = sdate.strftime("%m/%d/%Y")
    edate=date_time_obj = datetime.strptime(edate, '%Y-%m-%d')

    df = pd.DataFrame(list(mst_PPI100.objects.filter(Commodity=product_name,Date__gte=sdate,Date__lte=edate).values()))
    # import ipdb; ipdb.set_trace()

    # import ipdb;ipdb.set_trace()
    if df.empty:
        context="empty"
        return context

    # import ipdb; ipdb.set_trace()
    df=df.sort_values(by=['Date'], ascending=[False])
    df = df[['Product_Code','Commodity','industry','Unit','Value','Date']]
    df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')

    df=df.drop_duplicates(subset=None, keep='first', inplace=False)

    json_records = df.reset_index().to_json(orient ='records')
    # import ipdb;ipdb.set_trace()
    data = []
    data = json.loads(json_records)
    context = {'d': data}
    return context
