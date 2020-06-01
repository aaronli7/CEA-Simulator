# -*- coding: utf-8 -*-
from maps_app.simulator import Simulator, zip_file, adddatatodb
import sys,os

# The parameters from frontend:
# - result: json list {jday, hours, ghi}
# - CO2
# - Temperature
# - start_jday
# - end_jday
class sim:
    def start(self, co2, temp, result, start_jday, end_jday):
        CO2 = co2
        temp = temp
        result = result
        start_jday = start_jday
        end_jday = end_jday
        # print('Temperature', temp)
        tom_sim = Simulator(CO2, temp, result, start_jday, end_jday)


        # read basic parameter for simulation
        # tom_sim.read_config('/Users/aran-lq/CEAsimulator/mysite/server/src/config.ini')
        tom_sim.read_config(r'config.ini')


        # user prompt
        tom_sim.question()

        # read transfer information for greenhouse
        tom_sim.read_transref(r'config.ini')

        # read radiation file
        #tom_sim.read_radiation('global_radiation.csv')
        tom_sim.read_radiation()

        # simulation start
        tom_sim.start_simulation()

        # compress output file
        # zip_file('/Users/aran-lq/CEAsimulator/mysite/server/static/output/')
        zip_file()
        adddatatodb()

    def getFinalTruss():
        return tom_sim.initial_truss
