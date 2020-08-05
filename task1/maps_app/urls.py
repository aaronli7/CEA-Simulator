from django.conf.urls import url
from django.conf.urls import include
from django.urls import path
from maps_app import views
# from . import views
import json

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'grafana/', views.grafana, name='grafana'),
    url(r'home/', views.home, name='home'),
    url(r'table1/', views.table1, name='table1'),
    url(r'table2/', views.table2, name='table2'),
    url(r'register/', views.register, name='register'),
    url(r'mappage/', views.mappage, name='mappage'),
    url(r'mainpage/', views.mainpage, name='mainpage'),
    url(r'chart/', views.chart, name='chart'),
    url(r'energymodel/', views.energymodel, name='energymodel'),
    url(r'energysupply/', views.energysupply, name='energysupply'),
    url(r'page2/', views.page2, name='page2')
    # url(r'^$',views.table,name='table'),
]
