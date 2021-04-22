
import requests
import pandas as pd
import time
import os
import glob
import datetime
import requests

from datetime import date

from bs4 import BeautifulSoup


from django.conf import settings

from .models import mst_PPI100


def test():
    Product_Code=123
    Commodity="dummy"
    industry="chemical"
    Unit="dollar per pound"
    Value="123"
    Date=date.today()


def Scraped_100PPI_Data():



    path=settings.BASE_DIR + '/media/'
    dfmapname=pd.read_excel(path+'mapping.xlsx',sheet_name='name')

    dfmapnunit=pd.read_excel(path+'mapping.xlsx',sheet_name='unit')

    dfmapname['Code'] = dfmapname['Code'].astype(str)

    # startDate = date(2021, 3, 3)
    startDate = mst_PPI100.objects.latest("Date").Date.date()
    print(startDate)


    endDate=date.today()
    # endDate = date(2021, 3, 1)
    print(endDate)
    diff = (endDate - startDate).days + 1
    print(diff)
#    return

    dfError=pd.DataFrame()
    dfAllData=pd.DataFrame()

    for j in range(1,diff):


        xdt = startDate + pd.DateOffset(days= j)
        xyear = xdt.year
        xmonth=xdt.month
        xday = xdt.day

        strLink='http://top.100ppi.com/zdb/detail-day-' + str(xyear) + '-' +str('{:02d}'.format(xmonth))+str('{:02d}'.format(xday))+'-1.html'

        print(strLink)


        try:

            response = requests.get(strLink)
            columns = []
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            actDate = soup.find("div",class_="name2").text
            print(actDate)
            finaldt=actDate.replace("http://www.100ppi.com   ","").replace("生意社","")
            finaldt = datetime.datetime.strptime(finaldt, '%Y-%m-%d %H:%M:%S')

            finaldt=datetime.datetime.strftime(finaldt, '%Y-%m-%d')

            print('Find Date :' + finaldt)
            records = []
            for tr in table.findAll("tr"):
                trs = tr.findAll("td")
                record = []
                for each in trs:
                    try:
                        link = each.find('a')['href']
                        link = link.replace('http://www.100ppi.com/vane/detail-','')
                        link = link.replace('.html','')
                        text = each.text
                        record.append(str(link))
                        record.append(text)

                    except:
                        text = each.text
                        record.append(text)
                records.append(record)

            df = pd.DataFrame(data=records, columns = ['Code','Commodity', 'industry', 'Date1','Date2','Unit','Daily_ups_and_downs','YoY'])
            df['Date']=finaldt
            df=df[df['Code']!="商品"]
            dfAllData=dfAllData.append(df)



        except:
            dfError = dfError.append({'ErrorUrl':strLink}, ignore_index=True)

    # dfError.to_excel('Errorlog.xlsx',index=False)



    if dfAllData.empty==False:

        dfAllData=dfAllData.merge(dfmapname,on='Code')

        dfAllData=dfAllData.merge(dfmapnunit,on='Unit')

        dfAllData = dfAllData[["Code", "Unit", "En_Commodity","En_Industry", "En_unit","Date1","Date"]]

        row_iter = dfAllData.iterrows()

        objs = [

            mst_PPI100(
                Product_Code = row['Code'],

                Commodity  = row['En_Commodity'],
                industry  = row['En_Industry'],
                Unit  = row['En_unit'],
                Value  = row['Date1'],
                Date  = row['Date']
            )

            for index, row in row_iter
        ]

        mst_PPI100.objects.bulk_create(objs)


        # for df_loop in dfAllData.itertuples():
        #         agency = mst_PPI100.objects.create(Product_Code=df_loop.Code,Commodity=df_loop.En_Commodity,industry=df_loop.En_Industry,Unit=df_loop.En_unit,Value=df_loop.Date1,Date=df_loop.Date)

        dfAllData.to_excel('100PPI_Data.xlsx',index=False)
