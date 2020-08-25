from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import redirect
from influxdb import InfluxDBClient
from datetime import datetime
from maps_app.sim import sim
import pymysql
import json
import csv


client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('db1')
sim_obj = sim()

def index(request):
    return render(request,'maps_app/index.html')
# Create your views here.

def mainpage(request):
    return render(request,'maps_app/mainpage.html')

def chart(request):
    return render(request,'maps_app/chart.html')

def table1(request):
    user = str(request.user)
    return render(request,'maps_app/table1.html',{'username':user})

def table2(request):
    user = str(request.user)
    return render(request,'maps_app/table2.html',{'username':user})

def energymodel(request):
    return render(request,'maps_app/energymodel.html')

def energysupply(request):
    return render(request,'maps_app/energysupply.html')

def mappage(request):
    data_from_web_page = request.GET
    if data_from_web_page.__contains__('locationid'):
        user = str(request.user)
        date_from = data_from_web_page.get('datefrom')
        year_from = getyear(date_from)
        date_from_julian = converttojulian(date_from)
        date_to = data_from_web_page.get('dateto')
        year_to = getyear(date_to)
        date_to_julian = converttojulian(date_to)
        location_id = data_from_web_page.get('locationid')
        location_id = str(location_id) +"_"+ str(year_from)
        co2 = data_from_web_page.get('CO2')
        co2=float(co2)
        temperature = data_from_web_page.get('TEMPERATURE')
        temperature=float(temperature)
        result = client.query('Select "jday", "hour", "ghi" From "' + location_id + '" where jday>= '+str(date_from_julian)+' and jday<= '+str(date_to_julian))
        timeSeriesEpoch=[]
        jday=[]
        i=0
        for row in result:
            for r in row:

                timestamp=datetime.strptime(r['time'],"%Y-%m-%dT%H:%M:%SZ").timestamp()
                timeSeriesEpoch.insert(i,int(timestamp))
                jday.insert(i,r['jday'])
                i=i+1

        epochstart = min(timeSeriesEpoch)*1000
        epochend = max(timeSeriesEpoch)*1000
        start_jday = min(jday)
        end_jday = max(jday)
        sim_obj.start(user, co2, temperature, result, start_jday,end_jday)

        pytojsfruit = pythontojsfruit(user)
        pytojsgrowth = pythontojsgrowth(user)
        # print(pytojs)

        resp =render(request,'maps_app/chart.html',{'result': result,'username':user, 'pytojsfruit':pytojsfruit, 'pytojsgrowth':pytojsgrowth, 'temp':temperature, 'co2':co2})
        return resp
    return render(request, "maps_app/mappage.html")


def pythontojsfruit(user):
    filename = "static/"+user+"_FruitDev.csv"

    # initializing the titles and rows list
    fields = []
    rows = []

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)


    # print('Field 1 : '+fields[0])
    # print('Field 2 : '+fields[1])

    datapoints = "["

    for row in rows[:-3]:
        datapoints+="["
        for col in row[:2]:
            datapoints+=col + ","
        datapoints = datapoints[:-1]
        datapoints+="],"
    datapoints = datapoints[:-1]
    datapoints+="]"

    # print(datapoints)
    return datapoints

def pythontojsgrowth(user):
    filename = "static/"+user+"_growth.csv"

    # initializing the titles and rows list
    fields = []
    rows = []

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

    print('Field 1 : '+fields[0])
    print('Field 2 : '+fields[1])

    datapoints = "["

    for row in rows[:-3]:
        datapoints+="["
        for col in row[:2]:
            datapoints+=col + ","
        datapoints = datapoints[:-1]
        datapoints+="],"
    datapoints = datapoints[:-1]
    datapoints+="]"

    # print(datapoints)
    return datapoints


def converttojulian(date):
    dt = datetime.strptime(date,"%Y-%m-%d")
    tt = dt.timetuple()
    day=tt.tm_yday
    return day

def getyear(date):
    dt = datetime.strptime(date,"%Y-%m-%d")
    return dt.year

def grafana(request):
   return render(request, "maps_app/grafana.html")

def home(request):
    data_from_web_page = request.POST
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user=auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return render(request, "maps_app/mainpage.html")

        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, "maps_app/index.html")
    return render(request, "maps_app/index.html")



def register(request):
    data_from_web_page = request.POST
    # print("Request:" ,request.POST)
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Id already exists')
                    return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, password=password)
                user.save();
                messages.success(request,'Registration Success...Continue to Login')
                return redirect('register')
                # return render(request, "maps_app/mappage.html")
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    return render(request, "maps_app/index.html")

def page2(request):
   return render(request, "maps_app/page2.html")

def logout_view(request):
   logout(request)
   return render(request, "maps_app/index.html")
