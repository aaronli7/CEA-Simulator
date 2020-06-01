from django.conf.urls import url
from django.conf.urls import include
from django.urls import path
from maps_app import views
# from . import views
import json

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^$',views.home_view,name='home_view'),
    url(r'grafana/', views.grafana, name='grafana')
    # url(r'^$',views.table,name='table'),
]
