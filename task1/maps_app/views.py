from django.shortcuts import render
from django.http import HttpResponse
from influxdb import InfluxDBClient
from datetime import datetime
from maps_app.sim import sim
import json

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('db1')
sim_obj = sim()

def index(request):
    data_from_web_page = request.GET
    if data_from_web_page.__contains__('locationid'):
        date_from = data_from_web_page.get('datefrom')
        date_from_julian = converttojulian(date_from)
        date_to = data_from_web_page.get('dateto')
        date_to_julian = converttojulian(date_to)
        location_id = data_from_web_page.get('locationid')
        co2 = data_from_web_page.get('CO2')
        co2=float(co2)
        temperature = data_from_web_page.get('TEMPERATURE')
        temperature=float(temperature)
        result = client.query('Select "day", "hour", "ghi" From "' + location_id + '" where day>= '+str(date_from_julian)+' and day<= '+str(date_to_julian))
        timeSeriesEpoch=[]
        jday=[]
        i=0
        for row in result:
            for r in row:

                timestamp=datetime.strptime(r['time'],"%Y-%m-%dT%H:%M:%SZ").timestamp()
                timeSeriesEpoch.insert(i,int(timestamp))
                jday.insert(i,r['day'])
                i=i+1

        epochstart = min(timeSeriesEpoch)*1000
        epochend = max(timeSeriesEpoch)*1000
        start_jday = min(jday)
        end_jday = max(jday)
        sim_obj.start(co2, temperature, result, start_jday,end_jday)
        resp =render(request,'maps_app/table.html',{'result': result,'epochstart': epochstart , 'epochend' : epochend})
        return resp
    return render(request,'maps_app/index.html')
# Create your views here.
def home_view(request):
    print(request.GET)
    return render(request, "maps_app/index.html")


def converttojulian(date):
    dt = datetime.strptime(date,"%Y-%m-%d")
    tt = dt.timetuple()
    day=tt.tm_yday
    return day

def grafana(request):
   return render(request, "maps_app/grafana.html")
