from datetime import datetime
from time import gmtime, strftime
import pytz
import requests
from time import sleep
import json
date_format = '%Y-%m-%dT%H:%M:%S.%f%z'
local_tz = strftime('%z', gmtime())
local_tz = pytz.timezone('US/Pacific')

southwest = {'10251290':{'name': 'Borehole'},
             '10251300':{'name': 'Tecopa'},
             '10251330':{'name': 'China Ranch'},
             '10251335':{'name': 'Willow'},
             '355906115492601':{'name': 'Stump'},
             '360956115432801':{'name': 'Kiup'},
             '362727116013501':{'name':'Grapevine'},
             }

needs_work = ['362529116171100', '362727116013502'] #Devils hole well, Grapevine precip

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

def update_sites(sites):
    for site in sites:
        ld = get_most_recent_value(get_site_data(site).json())
        sites[site]['minutes'] = (datetime.now(local_tz) - ld).seconds / 60
    return sites

