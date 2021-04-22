import pandas as pd
import requests
from bs4 import BeautifulSoup

from datetime import datetime
from datetime import date
import os

from django.conf import settings

from .models import mst_sunsris

def test():
    import ipdb; ipdb.set_trace()
    Product_Code=123
    Commodity="dummy"
    industry="chemical"
    Unit="dollar per pound"
    Value="123"
    Date=date.today()



    mst_sunsris_var=mst_sunsris(Product_Code=Product_Code,Commodity=Commodity,industry=industry,Unit=Unit,Value=Value,Date=Date)

    mst_sunsris_var.save()


def Scraped_sunsris_Data():

    path=settings.BASE_DIR + '/media/'

    file_df = pd.read_excel(path + '/mapping_sunsris.xlsx')

    file_df['Link']=file_df['Link'].astype(int)

    # startDate = date(2020, 1, 1)

    startDate = mst_sunsris.objects.latest("Date").Date.date()

    # import ipdb; ipdb.set_trace()

    endDate=date.today()

    diff = (endDate - startDate).days + 1

    Alldata = pd.DataFrame()
    dfError=pd.DataFrame(columns=['ErrorUrl'])
    ErrRecord=[]
    # import ipdb; ipdb.set_trace()
    for j in range(1,diff):
        xdt = startDate + pd.DateOffset(days= j)
        xyear = xdt.year
        xmonth=xdt.month
        xday = xdt.day
        try:
            url='http://www.sunsirs.com/uk/sdetail-day-'+str(xyear)+'-'+str("{:02d}".format(xmonth))+str("{:02d}".format(xday))+'.html'
            print('links - '+str(url))
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            actDate = soup.find("div",class_="name").text.replace("100 Spot Commodities Price Chart  - ","")
            actDate=actDate.strip()
            table = soup.find('table')
            records = []
            for tr in table.findAll("tr"):
                trs = tr.findAll("td")
                record = []
                for each in trs:
                    try:
#                        link ="'"+ 'http://www.sunsirs.com/uk/'+each.find('a')['href']
                        link=each.find('a')['href'].replace('prodetail-','')
                        link=link.replace('.html','')
#                        print(link)
#                        break
                        text = each.text
                        record.append(link)
                        record.append(text)
                    except:
                        text = each.text
                        record.append(text)
                records.append(record)

            df = pd.DataFrame(data=records, columns = ['Link','Commodity', 'Sectors', 'Value','Value2','Change'])
            del df['Value2']
            del df['Change']

#            print(actDate)
            actDate=datetime.strptime(actDate, '%d/%m/%Y')


            df['Data_Date']=actDate #datetime.strptime(actDate, '%m-%d-%Y').date()
            df=df[df['Link']!="Commodity"]


            Alldata = Alldata.append(df)

        except:
            dfError = dfError.append({'ErrorUrl':url}, ignore_index=True)
            # pass


    if Alldata.empty==False:
        Alldata['Link']=Alldata['Link'].astype(int)
        Alldata = file_df.merge(Alldata,on='Link')

        Alldata['Commodity']=Alldata['Commodity1']
        del Alldata['Commodity1']
        print(Alldata)

        row_iter = Alldata.iterrows()

        objs = [

            mst_sunsris(
                Product_Code = row['Link'],

                Commodity  = row['Commodity'],
                industry  = row['Sectors'],
                Unit  = row['unit'],
                Value  = row['Value'],
                Date  = row['Data_Date']
            )

            for index, row in row_iter
        ]

        mst_sunsris.objects.bulk_create(objs)
    dfError.to_excel('Errorlog.xlsx',index=False)
