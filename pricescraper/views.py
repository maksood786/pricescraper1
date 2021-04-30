from django.shortcuts import render
from django.http import HttpResponse
from PPI100.models import mst_PPI100
import datetime
from datetime import date
from datetime import datetime
import pandas as pd
import json

def index(request):
    print('heloo')
    edate = date(2021, 3, 2)
    sdate = date(2021, 3,2)
    edate = edate.strftime("%Y-%m-%d")
    sdate = sdate.strftime("%Y-%m-%d")

    context=getComdata(sdate,edate)

    return render(request, 'main.html',context)

    # return render(request, 'main.html')

def contact(request):
    return render(request, 'contactus.html')

def getComdata(sdate,edate):

    sdate=date_time_obj = datetime.strptime(sdate, '%Y-%m-%d')
    # sdate = sdate.strftime("%m/%d/%Y")
    edate=date_time_obj = datetime.strptime(edate, '%Y-%m-%d')

    df = pd.DataFrame(list(mst_PPI100.objects.filter(Date__gte=sdate,Date__lte=edate).values()))
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
