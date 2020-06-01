import pandas as pd
import numpy as np
import sys, os
from IPython.display import display
from influxdb import InfluxDBClient

class data:
    def adddatatodb(self):
        client = InfluxDBClient(host='localhost', port=8086)
        client.switch_database('db1')

        df1=pd.read_csv('../static/tomsim_distri.csv')
        print(df1)
