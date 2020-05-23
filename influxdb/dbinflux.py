import pandas as pd
import numpy as np
import sys, os
from IPython.display import display
from influxdb import InfluxDBClient
from datetime import datetime
from dateutil import parser

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('db1')

df=pd.read_csv('Final.csv')

for row_ind, r in df.iterrows():
    lat = r[1]
    lon = r[2]
    year = '2014'
    api_key = 'q2NPd9Kwya8zJjjguq0Hwl8Dovn3GU8wk0HldbpX'
    attributes = 'ghi,dhi,dni,wind_speed,air_temperature,solar_zenith_angle'
    leap_year = 'false'
    interval = '60'
    utc = 'false'
    your_name = 'Aishwarya+Venkataraj'
    reason_for_use = 'research'
    your_affiliation = 'my+UGA'
    your_email = 'aishwaryavenkatraj@gmail.com'
    mailing_list = 'true'
    apiweather = '6e8d1092b595df64eaa6ca144eef1662'
    dfsolar = pd.read_csv('http://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes), skiprows=2)
    dfsolar = dfsolar.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=interval+'Min', periods=525600/int(interval)))
    dfsolar.index.names = ["Timestamp"]
    dfsolar.reset_index(drop=False, level='Timestamp', inplace=True)
    dfsolar['Date'] = pd.to_datetime(dfsolar['Timestamp']).dt.date
    dfsolar['Time'] = pd.to_datetime(dfsolar['Timestamp']).dt.time

    #print(dfsolar)
    for row_index, row in dfsolar.iterrows():
        ts = datetime(row[1], row[2], row[3], row[4], row[5]).timestamp()

        ts = str(ts)
        timestamp = ts.replace('.0', '')
        timestamp = timestamp
        #print(timestamp)
        dbname = r[0]
        fmt = '%Y-%m-%d'
        date = row[12]
        dt = datetime.strptime(str(date), fmt)
        tt = dt.timetuple()
        day=tt.tm_yday
        #print(day)
        # fieldvalue = row[0]
        # print(row[0])
        json_body = [
            {
                "measurement": dbname,

                "tags": {

                    "id": r[0],
                     "dhi": row[7],
                    "dni": row[8],
                    "wspeed": row[9],
                    "temperature": row[10],
                    "sza": row[11],
                    "Timestamp": row[0],
                    "date": row[12],


                 },

                "fields": {

                    "ghi": row[6],
                     "day": day,
                    "month": row[2],
                    "year": row[1],
                     "hour": row[4],
                    "minute": row[5]
                },
                "time": row[0]
            }
         ]
    #print(json_body)
        client.write_points(json_body, time_precision='s')

