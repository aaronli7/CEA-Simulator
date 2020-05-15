from django.shortcuts import render

from django.http import HttpResponse
from influxdb import InfluxDBClient
from datetime import datetime
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('db1')

def index(request):
    print(request.GET)
    data_from_web_page = request.GET
    if data_from_web_page.__contains__('locationid'):
        date_from = data_from_web_page.get('datefrom')
        date_fr = datetime.strptime(date_from, "%Y-%m-%d")
        date_to = data_from_web_page.get('dateto')
        date_t = datetime.strptime(date_to, "%Y-%m-%d")
        location_id = data_from_web_page.get('locationid')
        result = client.query('Select "day", "date", "ghi" From "' + location_id + '" where day>= '+str(date_fr.day)+' and month>= '+str(date_fr.month)+ ' and day<= '+str(date_t.day)+' and month<= '+str(date_t.month))
        # result = client.query('Select "day", "date", "ghi" From "' + location_id + '" where date>= '+str(date_from)+' and date<= '+str(date_to))
        print("DATA from Database", result)
        resp =render(request,'maps_app/table.html',{'result': result})
        return resp
        #return HttpResponse({'d':result}, 'maps_app/table.html', content_type=text/html")
    #print(date_from, date_to, location_id)
    return render(request,'maps_app/index.html')
# Create your views here.
def home_view(request):
    #print("hello world")
    print(request.GET)
    return render(request, "maps_app/index.html")
