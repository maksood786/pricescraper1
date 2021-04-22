from django.http import HttpResponse
from django.shortcuts import render
# from django.conf import settings
# from django.contrib import messages
# import requests
# import re
# import xml.etree.ElementTree as ET
import pandas as pd
import json
#
from datetime import datetime
from .scraper import test
from .scraper import Scraped_sunsris_Data
from .models import mst_sunsris
from django.contrib import messages

# Create your views here.
def index(request):

    if request.method == 'POST' and 'refresh' in request.POST:
        # return HttpResponse('page is under construction')
        # entries= mst_sunsris.objects.all()
        # entries.delete()     #delete entire data from table
        # import ipdb; ipdb.set_trace()
        Scraped_sunsris_Data()
        messages.success(request, 'data has been fetched successfully till latest date')

    context=getComname()
    return render(request,'indexsunsris.html',context)

def result(request):

    if request.method=="POST":
        sdate=request.POST.get("sdate")
        edate=request.POST.get("edate")
        product_name=request.POST.get("product_name")
        # import ipdb; ipdb.set_trace()
        context=getComdata(product_name,sdate,edate)

    if context=="empty":
        return render(request,'noresult.html')
    else:
        return render(request,'result.html',context)

def getComname():

    df = pd.DataFrame(list(mst_sunsris.objects.values_list('Commodity')),columns =['commodity'])
    df=df.drop_duplicates(subset=None, keep='first', inplace=False)
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
    return context

def getComdata(product_name,sdate,edate):

    sdate=date_time_obj = datetime.strptime(sdate, '%Y-%m-%d')
    # sdate = sdate.strftime("%m/%d/%Y")
    edate=date_time_obj = datetime.strptime(edate, '%Y-%m-%d')

    df = pd.DataFrame(list(mst_sunsris.objects.filter(Commodity=product_name,Date__gte=sdate,Date__lte=edate).values()))


    # import ipdb;ipdb.set_trace()
    if df.empty:
        context="empty"
        return context

    df=df.sort_values(by=['Date'], ascending=[False])
    # import ipdb; ipdb.set_trace()
    df = df[['Product_Code','Commodity','industry','Unit','Value','Date']]
    df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')

    df=df.drop_duplicates(subset=None, keep='first', inplace=False)

    json_records = df.reset_index().to_json(orient ='records')
    # import ipdb;ipdb.set_trace()
    data = []
    data = json.loads(json_records)
    context = {'d': data}
    return context
