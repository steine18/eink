from datetime import datetime
from time import gmtime, strftime
import pytz
import requests
from time import sleep
import json
date_format = '%Y-%m-%dT%H:%M:%S.%f%z'
local_tz = strftime('%z', gmtime())
local_tz = pytz.timezone('US/Pacific')

southwest = {'10251290':{},
             '10251300':{},
             '10251330':{},
             '10251335':{},
             '355906115492601':{},
             '360956115432801':{},
             '362727116013501':{'name':'Kiup'},
             }

needs_work = ['362529116171100', '362727116013502'] #Devils hole well, kiup precip

sites=['094196784', '094196783']

def get_site_data(site):
    url = f'https://waterservices.usgs.gov/nwis/iv/?format=json&sites={site}&parameterCd=00060,00065&agencyCd=USGS&siteStatus=all'
    r = requests.get(url)
    return r

def get_most_recent_value(ts_json):
    data_sets = [datetime.strptime(ds['values'][0]['value'][0]['dateTime'], date_format) for ds in ts_json['value']['timeSeries']]
    return list(set(data_sets))[0]

def time_since_last(dt):
    return (datetime.now(local_tz) - dt).seconds/60

def get_time(sites):
    s = [time_since_last(get_most_recent_value(get_site_data(site).json())) for site in sites]
    return s

df = [get_most_recent_value(get_site_data(site).json()) for site in southwest]

for site in southwest:
    ld = get_most_recent_value(get_site_data(site).json())
    print((datetime.now(local_tz) - ld).seconds/ 60)


ld = get_most_recent_value(df.json())
(datetime.now(local_tz) - list(set(ld))[0]).seconds) / (60*60)