import configparser, json, csv, math, sys, os
import shutil
import zipfile
from os.path import join, getsize
import pandas as pd
import numpy as np
from IPython.display import display
from influxdb import InfluxDBClient

# compress all the file into zip
def zip_file():
    zip_name = os.path.abspath(os.path.join(os.getcwd(),'static/report.zip'))
    src_dir = os.path.abspath(os.path.join(os.getcwd(),'static/'))
    # zip_name = '/Users/aran-lq/CEAsimulator/mysite/server/static/' +'report.zip'
    z = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(src_dir):
        fpath = dirpath.replace(src_dir,'')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
    z.close()

PI = 3.141592654
# constant definition
LAT = 52
IAGE = [0] * 75

def adddatatodb():
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('db1')

    df1 = pd.read_csv('static/tomsim_distri.csv')
    df2 = pd.read_csv('static/tomsim_FruitDev.csv')
    df3 = pd.read_csv('static/tomsim_growth.csv')

    for row_index, r in df1.iterrows():
        json_body = [
            {
                "measurement": "tomsim_distri",

                "tags": {

                    "GTWOLD": r[5],
                    "WTW": r[6],
                    "WLV": r[7],
                    "WST": r[8],
                    "WSO": r[9],
                    "BUFFER": r[10],
                    "NRVEGUNITS": r[14],
                    "TRUSS_1": r[15],
                    "TRUSS_2": r[16],
                    "TRUSS_3": r[17],
                    "TRUSS_4": r[18],
                    "TRUSS_5": r[19],
                    "TRUSS_6": r[20],
                    "TRUSS_7": r[21],
                    "TRUSS_8": r[22],
                    "TRUSS_9": r[23],
                    "TRUSS_10": r[24],
                    "TRUSS_11": r[25],
                    "TRUSS_12": r[26],
                    "TRUSS_13": r[27],
                    "TRUSS_14": r[28],
                    "TRUSS_15": r[29],
                    "TRUSS_16": r[30],
                    "TRUSS_17": r[31],
                    "TRUSS_18": r[32],
                    "TRUSS_19": r[33],
                    "TRUSS_20": r[34],
                    "TRUSS_21": r[35],
                    "TRUSS_22": r[36],
                    "TRUSS_23": r[37],
                    "TRUSS_24": r[38],
                    "TRUSS_25": r[39],
                    "TRUSS_26": r[40],
                    "TRUSS_27": r[41],
                    "TRUSS_28": r[42],
                    "TRUSS_29": r[43],
                    "TRUSS_30": r[44],
                    "TRUSS_31": r[45],
                    "TRUSS_32": r[46],
                    "TRUSS_33": r[47],
                    "TRUSS_34": r[48],
                    "TRUSS_35": r[49],
                    "WTRUSS_615": r[50],
                    "WVEGUNIT_1": r[51],
                    "WVEGUNIT_2": r[52],
                    "WVEGUNIT_3": r[53],
                    "WVEGUNIT_4": r[54],
                    "WVEGUNIT_5": r[55],
                    "WVEGUNIT_6": r[56],
                    "WVEGUNIT_7": r[57],
                    "WVEGUNIT_8": r[58],
                    "WVEGUNIT_9": r[59],
                     "WVEGUNIT_10": r[60],
                    "WVEGUNIT_11": r[61],
                    "WVEGUNIT_12": r[62],
                    "WVEGUNIT_13": r[63],
                    "WVEGUNIT_14": r[64],
                    "WVEGUNIT_15": r[65],
                    "WVEGUNIT_16": r[66]


                 },

                "fields": {
                    "JDAY": r[0],
                    "FRVEG": r[1],
                    "TOTALVEG": r[2],
                    "TOTAL": r[3],
                    "SLA": r[4],
                    "TRNR": r[11],
                    "TMPA": r[12],
                    "CO2": r[13]
                },
            }
         ]

        client.write_points(json_body, time_precision='s')
    for row_index, r in df2.iterrows():
        json_body = [
            {
                "measurement": "tomsim_FruitDev",

                "tags": {


                    "AVTEMP": r[2],
                     "IAGE": r[3]

                 },

                "fields": {
                    "JDAY": r[1],
                    "TRNR": r[0]
                },
            }
         ]

        client.write_points(json_body, time_precision='s')
    for row_index, r in df3.iterrows():
        json_body = [
            {
                "measurement": "tomsim_growth",

                "tags": {

                    "AVRAD": r[1],
                    "TEMP": r[2],
                    "CO2": r[3],
                    "FGMAX": r[4],
                    "EFF": r[5],
                    "LAI": r[7],
                    "GPHOT": r[8],
                    "RGR_AV": r[9],
                    "MAINT": r[10],
                    "GTW": r[11],
                    "WTW": r[12],
                    "WTW-WRT": r[13],
                    "WLV": r[14],
                    "WLV+WST": r[15],
                    "WSO": r[16],
                    "WRT": r[17],
                    "WLVE": r[18],
                    "WSTE": r[19],
                    "WSOE": r[20],
                    "DPARDF": r[21],
                    "DPARDR": r[22]


                 },

                "fields": {
                    "JDAY": r[0],
                    "SLA": r[6],
                    "TRNR": r[12],
                    "TMPA": r[13],
                    "CO2": r[14]
                },
            }
         ]

        client.write_points(json_body, time_precision='s')

class Simulator:
    # simulator attributes
    def __init__(self, CO2, temp, result, start_jday, end_jday):
        print("I am simulator of you!")
        # To be input by user
        self.CO2 = CO2
        self.temp = temp
        self.NRFRT = 0
        self.start_time = start_jday
        self.finish_time = end_jday
        self.result = result

        # some initial parameters
        self.NRVEGUNITS = 0
        # array parameters
        self.IAVRAD = 730
        self.NRFRTS = [0] * 75
        self.WVEGUNIT = [0] * 75
        # truss and vegetative position
        self.TRUSS_POS = 100
        self.VEG_POS = 100
        self.WTRUSS = [0] * 75
        self.SINK = [0] * 75
        self.SINKVEG = [0] * 75
        self.DEV = [0] * 75

        self.ITG = [0] * 75
        self.ITGVEG = [0] * 75
        self.GRVEG = [0] * 75
        self.GRTRUSS = [0] * 75

        self.GLOB = [0] * 24
        self.DTEMP = [0] * 24
        self.DCO2 = [0] * 24
        self.TEMP = [0] * 200

        # greenhouse transmission paramters
        self.EL = [0] * 20
        self.NAZ = [0] * 20
        self.AZ = [[0] * 20 for _ in range(20)]
        self.TC = [[0] * 20 for _ in range(20)]
        self.TG = [[0] * 20 for _ in range(20)]

        # general option
        self.SELYEAR = True
        self.LAICALC = False
        self.FIXEDCROP = True
        self.MANUAL_LEAF_PICKING = False
        self.SIDE_SHOOT = False
        self.INITATION = False

        # some assignment to be fixed   aaronli
        self.FSTT = [0] * 730
        self.FRTT = [0] * 730
        self.FSOT = [0] * 730
        self.LAIT = [0] * 730
        # table with SLA (cm2/g)
        self.SLAT = [0] * 730
        self.ISLAT = len(self.SLAT)
        self.LAIT = [0] * 730
        self.ILAIT = len(self.LAIT)
        # table with cumulative harvest of leaves, stems and storage organs (g/m2)
        self.WLVP = [0] * 730
        self.WSTP = [0] * 730
        self.WSOP = [0] * 730
        self.PDVU = [0] * 730
        self.RGR = [0] * 730
        self.BUFFER = 0
        self.WTRUSS615 = 0

        # climate data initialize
        # GLOTAB（radiation day, hour)
        # GLOSTAB(radiation sum per day)
        # TEMPTAB(temperature, day, hour)
        # AVTEMP（average temperature per day）
        # CO2TAB(CO2, day, hour)
        # CO2D(average CO2 per day)
        self.GLOTAB = [[0] * 24 for _ in range(730)]
        self.GLOSTAB = [0] * 730
        self.TEMPTAB = [[0] * 24 for _ in range(730)]
        self.AVTEMP = [0] * 730
        self.CO2TAB = [[0] * 24 for _ in range(730)]
        self.CO2D = [0] * 730

    def read_config(self, filename):
        print("I am reading config file ")

        # fix the directory problem
        config_file = os.path.abspath(os.path.join(os.getcwd(),'maps_app/',filename))
        cf = configparser.ConfigParser()
        cf.read(config_file, encoding='UTF-8')
        # member variable assignment
        # print(os.getcwd())
        self.KDIF = json.loads(cf.get('simulation', 'KDIF'))
        self.SCV = json.loads(cf.get('simulation', 'SCV'))
        self.MAINLV = json.loads(cf.get('simulation', 'MAINLV'))
        self.MAINST = json.loads(cf.get('simulation', 'MAINST'))
        self.MAINSO = json.loads(cf.get('simulation', 'MAINSO'))
        self.MAINRT = json.loads(cf.get('simulation', 'MAINRT'))
        self.Q10 = json.loads(cf.get('simulation', 'Q10'))
        self.REFTMP = json.loads(cf.get('simulation', 'REFTMP'))
        self.ASRQLV = json.loads(cf.get('simulation', 'ASRQLV'))
        self.ASRQST = json.loads(cf.get('simulation', 'ASRQST'))
        self.ASRQSO = json.loads(cf.get('simulation', 'ASRQSO'))
        self.ASRQRT = json.loads(cf.get('simulation', 'ASRQRT'))
        self.WLV = json.loads(cf.get('simulation', 'WLV'))
        self.WST = json.loads(cf.get('simulation', 'WST'))
        self.WSO = json.loads(cf.get('simulation', 'WSO'))
        self.WRT = json.loads(cf.get('simulation', 'WRT'))
        self.PLDENS = json.loads(cf.get('simulation', 'PLDENS'))
        #self.start_time = json.loads(cf.get('simulation', 'start_time'))
        #self.finish_time = json.loads(cf.get('simulation', 'finish_time'))
        self.DELT = json.loads(cf.get('simulation', 'DELT'))
        self.PRDEL = json.loads(cf.get('simulation', 'PRDEL'))
        self.FRLV = json.loads(cf.get('simulation', 'FRLV'))
        self.initial_truss = json.loads(cf.get('simulation', 'initial_truss'))
        self.STTRU = json.loads(cf.get('simulation', 'STTRU'))
        self.FSINK = json.loads(cf.get('simulation', 'FSINK'))

        return

    def read_radiation(self):
        #print("I am reading radiation file from the data base ")
        #pass
        #config_file = os.path.abspath(os.path.join(os.getcwd(), filename))

        # temporary read in CSV format
        #with open(config_file, 'r') as f:
        #f_csv = csv.reader(f)
        global_sum = 0
        TG = 0
        CG = 0
        ANTAL = 0
        rad_data = self.result
        # csv file loop
        for rad_row in rad_data:
            for row in rad_row:
            # [num_day, num_hours, radiation] = [int(float(row[0])), int(float(row[1])), float(row[2])]
                [num_day, num_hours, radiation] = [row['jday'], row['hour'], row['ghi']]
                if num_hours == 0:
                    global_sum = 0
                    TG = 0
                    ANTAL = 0
                    CG = 0
                self.GLOTAB[num_day - 1][num_hours ] = radiation
                self.CO2TAB[num_day - 1][num_hours ] = self.CO2
                self.TEMPTAB[num_day - 1][num_hours] = self.temp
                global_sum += radiation
                # print('Self temp',self.temp)
                TG += self.temp
                # print('TG' , type(TG))
                if 0 < num_hours <= 23:
                    CG += self.CO2
                    ANTAL += 1
                if num_hours == 23:
                    global_sum *= 0.36
                    self.GLOSTAB[num_day - 1] = global_sum
                    self.AVTEMP[num_day - 1] = TG / 24
                    # print('Average Temp', self.AVTEMP[num_day - 1])
                    self.CO2D[num_day - 1] = CG / ANTAL
        return

    def read_transref(self, filename):
        print("I am reading transmission file for green house")
        config_file = os.path.abspath(os.path.join(os.getcwd(),'maps_app/', filename))
        cf = configparser.ConfigParser()
        cf.read(config_file)
        self.TRDIF = json.loads(cf.get('greenhouse', 'TRDIF'))
        self.AZIMGH = json.loads(cf.get('greenhouse', 'AZIMGH'))
        self.NEL = json.loads(cf.get('greenhouse', 'NEL'))
        self.EL = json.loads(cf.get('greenhouse', 'EL'))
        self.NAZ = json.loads(cf.get('greenhouse', 'NAZ'))
        self.AZ = json.loads(cf.get('greenhouse', 'AZ'))
        self.TC = json.loads(cf.get('greenhouse', 'TC'))
        self.TG = json.loads(cf.get('greenhouse', 'TG'))

        return

    # Ask user for the basic parameters setting
    def question(self):
        answer = True
        print("use of selyear or climatic data from experiments >> fixed to True")
        if not answer:
            print("answer is false")
            self.SELYEAR = False
        answer = False
        print("Calculations with fixed crop size? (Y/n) >>> fixed to N")
        if not answer:
            self.FIXEDCROP = False
        if not self.FIXEDCROP:
            answer = True
            print("Calculate LAI from SLA (y/N)? >>> fixed to Y")
            if answer:
                self.LAICALC = True
            answer = True
            print("Calculate SLA from standard? (y/N) >>> fixed to Y")
            if answer:
                self.SLAFUNCT = True

        answer = False
        print("Leaf picking by hand (y/N) >>> fixed to N")
        if answer:
            self.MANUAL_LEAF_PICKING = True
        answer = False
        print("Additional side_shoots (y/n) >>> fixed to N")
        if answer:
            self.SIDE_SHOOT = True
        # define by user
        # self.CO2 = float(input("Please input the CO2 value:"))
        # self.temp = float(input("Please input the temperature value:"))
        # self.NRFRT = int(input("Please give number of fruits per truss:"))
        self.NRFRT = 7

        return

    def pre_simulation(self):
        self.TIME = self.start_time
        self.ICOUNT = 1
        self.ICOUNT1 = 1
        # bypass question for parameters correction
        # correction on number of fruits
        self.CORNRFRTS = 1.0
        # correction on leaf picking
        self.CORBLAD = 1.0

        for i in range(50):
            self.NRFRTS[i] = self.NRFRT * self.CORNRFRTS
        # dry weight of total plants
        self.WTW = self.WLV + self.WST + self.WSO + self.WRT
        self.WLVE = self.WLV
        self.WVEGUNIT[0] = (self.WLV + self.WST) * 0.7
        self.WVEGUNIT[1] = (self.WLV + self.WST) * 0.2
        self.WVEGUNIT[2] = (self.WLV + self.WST) * 0.1
        self.WSTE = self.WST
        self.WSOE = self.WSO
        self.WTRUSS[0] = self.WSO
        self.RGRSOM = 0

        # bypass question = answer fixed
        # A always 1, B=33 means maint.resp dependent on RGR
        self.A = 1.0
        self.B = 33.0

        # correction on greenhouse transmissivity
        self.TRANSCOR = 1.13
        # correction on maintenance respiration
        self.CORMAINT = 1.0
        # correction on growth respiration
        self.CORGROWTHRESP = 1.0
        # correction on vegetative sink
        self.CORVEGSINK = 1.0
        # correction on irradiance
        self.CORRADIANCE = 1.0
        # correction on temperature
        self.CORTEMP = 1.0
        # correction on CO2
        self.CORCO2 = 1.0
        # correction on plant density
        self.CORPLDENS = 1.0
        # correction on SLA (SLA-function normalized)
        self.CORSLA = 1.0
        # correction on flowering rate
        self.CORFR = 1.0
        # correction on fruit development stage
        self.CORDEV = 1.0

        # which ground reflection coefficient
        self.REFGR = 0.5

        if self.SIDE_SHOOT:
            # flowering day side-shoot
            self.DATE_FLOWER_SHOOT = 100
            self.PLDENS2 = 3.125
            self.PLDENS = self.PLDENS2

        self.PLDENS = self.PLDENS * self.CORPLDENS
        return

    def lint(self, TABLE, ILTAB, X):
        # check on odd ILTAB
        if ILTAB % 2 != 0:
            print("ERROR in function LINT: ILTAB = {}, must be even!".format(ILTAB))
            quit()

        IUP = 0
        for i in range(3, ILTAB + 1, 2):
            if TABLE[i - 1] <= TABLE[i - 3]:
                print("X-coordinates not in ascending order at element {},".format(i))
                quit()
            if IUP == 0 and TABLE[i - 1] >= X:
                IUP = i

        if X < TABLE[0]:
            print("Interpolation below defined region!!")
            print("lint-function contains {} points, Interpolation at X=".format(ILTAB, X))
            return TABLE[1]

        if X > TABLE[ILTAB - 1 - 1]:
            print("Interpolation above defined region!!")
            print("lint-function contains {} points, Interpolation at X=".format(ILTAB, X))
            return TABLE[ILTAB - 1]
        slope = (TABLE[IUP + 1 - 1] - TABLE[IUP - 1 - 1]) / (TABLE[IUP - 1] - TABLE[IUP - 2 - 1])
        return TABLE[IUP - 1 - 1] + (X - TABLE[IUP - 2 - 1]) * slope

    def astrog(self, day, LATRAD):
        RAD = 0.017453292
        if LATRAD > 67 * RAD:
            print("ERROR in ASTROG: LAT > 67")
            quit()
        if LATRAD < -67 * RAD:
            print("ERROR in ASTROG: LAT > 67")
            quit()

        # declination of the sun as function of daynumber (DAYNR)
        self.DEC = - math.asin(math.sin(23.45 * RAD) * math.cos(2 * PI * (day + 10) / 365))

        # SINLD, COSLD and AOB are intermediate variables
        self.SINLD = math.sin(LATRAD) * math.sin(self.DEC)
        self.COSLD = math.cos(LATRAD) * math.cos(self.DEC)
        AOB = self.SINLD / self.COSLD

        # daylength(h)
        DAYL = 12 * (1 + 2 * math.asin(AOB) / PI)
        self.DSINB = 3600 * (DAYL * self.SINLD + 24 * self.COSLD * math.sqrt(1 - AOB * AOB) / PI)
        self.DSINBE = 3600 * (DAYL * (self.SINLD + 0.4 * (self.SINLD * self.SINLD + self.COSLD * self.COSLD * 0.5)) + \
                              12 * self.COSLD * (2 + 3 * 0.4 * self.SINLD) * math.sqrt(1 - AOB * AOB) / PI)
        self.SOLARC = 1370 * (1 + 0.033 * math.cos(2 * PI * day / 365))

        return

    # Calculation of deviation of solar time as a result of variation
    # of length of solar day during the year because of
    # excentricity of elliptical track of earth around sun, and because of
    # obliquity of ecliptical plane of earth.
    def timedev(self, day):
        if 1 <= day <= 106:
            return (-14.2 / 60) * math.sin((day + 7) * PI / 111)
        elif 107 <= day <= 166:
            return (4 / 60) * math.sin((day - 106) * PI / 59)
        elif 167 <= day <= 246:
            return (-6.5 / 60) * math.sin((day - 166) * PI / 80)
        elif 247 <= day <= 366:
            return (16.4 / 60) * math.sin((day - 247) * PI / 113)
        return

    def sunpos(self):
        RD = PI / 180
        # Sine of solar elevation (inclination)
        self.SINB = self.SINLD + self.COSLD * math.cos(2 * PI * (self.SOLHR + 12) / 24)
        self.BETA = math.asin(self.SINB)

        # solar azimuth
        COSAZ = - (math.sin(self.DEC * RD) - math.sin(LAT * RD) * self.SINB) \
                / (math.cos(LAT * RD) * math.cos(self.BETA))
        if COSAZ < -1.0:
            COSAZ = -1.0
        elif COSAZ > 1.0:
            COSAZ = 1.0
        self.AZIM = math.acos(COSAZ)

        if self.SOLHR <= 12:
            self.AZIM = -self.AZIM

        if self.SINB < 0:
            self.SINB = 0
        return

    def onev(self, Y, Z, YAR, NY):
        for i in range(NY):
            if Y < YAR[i]:
                break
        if i == NY - 1:
            return Z[NY - 1]

        if (i == 0):
            return Z[0]
        else:
            return Z[i - 1] + (Z[i] - Z[i - 1]) * (Y - YAR[i - 1])/(YAR[i] - YAR[i - 1])


    # Interpolation procedure for calculation of transmission of greenhouse
    # cover for direct radiation.
    def transd(self):
        RAD = 0.017453292
        # adaptation of azimuth depending on orientation of greenhouse
        self.AZIM = self.AZIM - self.AZIMGH * RAD

        #Conversion to degrees
        A1 = self.AZIM / RAD
        A1 = A1 % 180
        E = self.BETA / RAD

        # If necessary, mirroring of azimuth of sun
        if 90 <= A1 <= 180:
            A = 180 - A1
        if -90 < A1 < 0:
            A = - A1
        if -180 <= A1 <= -90:
            A = 180 + A1
        if 0 < A1 < 90:
            A = A1

        # Search for layer number (layers at 2.5, 7.5, .. , etc. degrees elevation)
        for i in range(self.NEL):
            if E < self.EL[i]:
                IXMIN = max(i-1, 1)
                IXMAX = i
                break
        if i == self.NEL - 1:
            IXMIN = self.NEL
            IXMAX = self.NEL

        # Interpolation in azimuth  problem?? aaronli
        TC1 = self.onev(A, self.TC[IXMIN - 1], self.AZ[IXMIN - 1], self.NAZ[IXMIN - 1])
        TG1 = self.onev(A, self.TG[IXMIN - 1], self.AZ[IXMIN - 1], self.NAZ[IXMIN - 1])

        if IXMIN == IXMAX:
            self.TRNSCN = TC1
            self.TRNSGL = TG1
        else:
            TC2 = self.onev(A, self.TC[IXMAX - 1], self.AZ[IXMAX - 1], self.NAZ[IXMAX - 1])
            TG2 = self.onev(A, self.TG[IXMAX - 1], self.AZ[IXMAX - 1], self.NAZ[IXMAX - 1])
            # Interpolation in elevation
            self.TRNSCN = TC1 + (TC2 - TC1) * (E - self.EL[IXMIN - 1])/(self.EL[IXMAX - 1]-self.EL[IXMIN - 1])
            self.TRNSGL = TG1 + (TG2 - TG1) * (E - self.EL[IXMIN - 1]) / (self.EL[IXMAX - 1] - self.EL[IXMIN - 1])
        return

    # * Purpose:
    # *   Calculation of fraction diffuse in global radiation from relation of
    # *   hourly values of atmosferic transmission versus hourly values of fraction
    # *   diffuse
    def fracdf(self, SOLARC, GRAD, SINELV):
        SO = SOLARC * SINELV
        ATMTR = GRAD / SO
        FRACDF = 1.47 - 1.66 * ATMTR
        if 0.35 >= ATMTR > 0.22:
            FRACDF = 1 - 6.4 * (ATMTR - 0.22)**2
        elif ATMTR <= 0.22:
            FRACDF = 1
        FRACDF = max(FRACDF, 0.15 + 0.85 * (1 - math.exp(-0.1 / SINELV)))

        return FRACDF

    def lphcur(self, TLEAF, CO2AIR):
        EFF0 = 0.017
        RS = 50
        RB = 100
        RD20 = 0.05
        Q10RD = 2.0

        # list for temperature dependence of mesophyll conductance
        GMT = [0, 0, 5, 0, 15, 0.004, 25, 0.004, 40, 0, 100, 0]

        # * Table for temperature dependence of maximal endogenous
        # * photosynthetic capacity
        PMMT = [0., 0., 5., 0., 15., 2., 25., 2., 40., 0., 100., 0.]

        # conductance GM is a function of temperature
        GM = self.lint(GMT, 12, TLEAF)
        # RM is the mesophyll resistance to CO2 assimilation
        if GM < 0.00001:
            RM = 3.0 * 10 ** 30
        else:
            RM = 1/GM

        # * Endogenous photosynthetic capacity PMM (mg CO2 m-2 s-1)
        # * is a function of temperaure
        PMM = self.lint(PMMT, 12, TLEAF)

        # CO2 compensation point increases with temperature
        GAMMA = 42.7 + 1.68 * (TLEAF - 25) + 0.012 * (TLEAF - 25)**2

        # Reduction of licht use efficiency by photorespiration
        CO2 = max(CO2AIR, GAMMA)
        self.EFF = EFF0 * (CO2 - GAMMA) / (CO2 + 2 * GAMMA)

        # * PNC is maximum as determined by CO2 diffusion
        # * 1.830 is mg CO2 per M3 per vpm
        # * stomatal resistance and boundary layer resistance to CO2 are 1.6 and 1.36
        # * times larger than to water vapour, respectively
        PNC = (CO2 - GAMMA) * 1.830 / (RM+1.36*RB+1.6*RS)

        if PMM < 0.00001:
            PNMAX = 0
        else:
            PNMAX = min(PNC, PMM)

        RD = RD20 * Q10RD ** (0.1 * (TLEAF - 20))
        self.FGMAX = PNMAX + RD

        return

    # *  Purpose: This subroutine performs a Gaussian integration over     *
    # *           depth of canopy by selecting three different LAI's and   *
    # *           computing assimilation at these LAI levels. The          *
    # *           integrated variable is FGROS.
    def assimr(self):
        # Gauss weights for three point Gauss

        IGAUSS = 3
        XGAUSS = [0.1127, 0.5000, 0.8873]
        WGAUSS = [0.2778, 0.4444, 0.2778]

        # Prevent math overflow; name change to prevent change of variable value
        SINEL = max(0.02, self.SINB)

        # reflection of horizontal and spherical leaf angle distribution
        SQV = math.sqrt(1 - self.SCV)
        REFH = (1 - SQV) / (1 + SQV)
        REFS = REFH * 2 / (1 + 1.6 * SINEL)

        KDIRBL = (0.5 / SINEL) * self.KDIF / (0.8 * SQV)
        KDIRT = KDIRBL * SQV

        T1 = math.exp(-self.KDIF * self.LAI)
        T2 = math.exp(- KDIRT * self.LAI)
        T3 = T1
        CORR1 = (REFH - self.REFGR) / (self.REFGR - 1 / REFH) * T1 * T1
        CORR2 = -REFS * REFS * T2 * T2
        CORR3 = -REFH * REFH * T3 * T3
        RE1 = (REFH + CORR1 / REFH) / (1. + CORR1)
        RE2 = (REFS + CORR2 / REFS) / (1. + CORR2)
        RE3 = (REFH + CORR3 / REFH) / (1. + CORR3)
        TE1 = T1 * (REFH * REFH - 1.) / (REFH * self.REFGR - 1.) / (1. + CORR1)
        TE2 = T2 * (1. - REFS * REFS) / (1. + CORR2)
        TE3 = T3 * (1. - REFH * REFH) / (1. + CORR3)

        PHIU = self.REFGR * self.PARDIR * TE2 / (1. - RE3 * self.REFGR)

        self.FGROS = 0
        for I1 in range(IGAUSS):
            LAIC = self.LAI * XGAUSS[I1]

            # absorbed fluxes per unit leaf area: diffuse flux, total direct
            # flux, direct component of direct flux.
            VISDF = (1 - REFH) * self.KDIF * (self.PARDIF * (math.exp(-self.KDIF * LAIC) + \
                CORR1 * math.exp(self.KDIF * LAIC)/REFH) / (1 + CORR1) + \
                PHIU * (math.exp(self.KDIF * (LAIC - self.LAI)) + CORR3 * math.exp(self.KDIF * (self.LAI - LAIC))/REFH)\
                /(1 + CORR3))
            VIST = (1 - REFS) * self.PARDIR * KDIRT * (math.exp(-KDIRT * LAIC) + CORR2 * math.exp(KDIRT * LAIC) / REFS)\
            / (1 + CORR2)
            VISD = (1 - self.SCV) * self.PARDIR * KDIRBL * math.exp(-KDIRBL * LAIC)

            # absorbed flux (J/M2 leaf/s) for shaded leaves and assimilation of
            # shaded leaves
            VISSHD = VISDF + (VIST - VISD)
            FGRSH = self.FGMAX * (1 - math.exp(-VISSHD * self.EFF / self.FGMAX))

            # direct flux absorbed by leaves perpendicular on direct beam and
            # assimilation of sunlit leaf area

            VISPP = (1 - self.SCV) * self.PARDIR / SINEL
            FGRSUN = 0
            for I2 in range(IGAUSS):
                VISSUN = VISSHD + VISPP * XGAUSS[I2]
                FGRS = self.FGMAX * (1 - math.exp(-VISSUN * self.EFF / self.FGMAX))
                FGRSUN = FGRSUN + FGRS * WGAUSS[I2]

            FSLLA = math.exp(-KDIRBL * LAIC)
            FGL = FSLLA * FGRSUN + (1 - FSLLA) * FGRSH

            # integration of local assimilation rate to canopy assimilation (FGROS)
            self.FGROS = self.FGROS + FGL * WGAUSS[I1]

        self.FGROS = self.FGROS * self.LAI

        return










    def totass(self, day):
        RAD = 0.017453292

        # unit of DEC changed from radians to degrees
        self.DEC /= RAD
        LONG = 5.7

        # assimilation set to zero and three different times of the day (HOUR)
        self.DPARDF = 0
        self.DPARDR = 0
        self.DTGA = 0
        self.SGSOM = 0

        for i in range(1, 25):
            IHOUR = i
            self.SOLHR = IHOUR - (1 - LONG / 15) + self.timedev(day)

            # call sunposition subroutine
            self.sunpos()

            if self.SINB >= 0.001:
                self.transd()

                #calculate global radiation outside
                SG = self.GLOB[IHOUR - 1]
                self.SGSOM += SG * 3600
                # calculate fraction diffuse radiation
                self.FRDIF = self.fracdf(self.SOLARC, SG, self.SINB)

                # diffuse PAR (PARDF) and direct PAR (PARDR)
                PAR = 0.47 * SG
                PARDF = self.FRDIF * PAR
                PARDR = (1.0 - self.FRDIF) * PAR

                # light climate inside the greenhouse, multiplication with greenhouse
                self.PARDIF = PARDF * self.TRDIF * self.TRANSCOR
                self.TRDIR = self.TRNSCN * self.TRNSGL
                self.PARDIR = PARDR * self.TRDIR * self.TRANSCOR

                # *-----Photosynthesis
                # *-----Determine EFF and FGMAX value of leaf photosynthesis-light response
                # *-----curve from temperature and CO2 concentration
                # *-----Leaf temperature is assumed equal to air temperature
                TL = self.DTEMP[i - 1]
                CO2 = self.DCO2[i - 1]
                self.lphcur(TL, CO2)

                # instantaneous assimilation
                self.assimr()
            else:
                self.FGROS = 0
                self.PARDIF = 0
                self.PARDIR = 0

            # *-----integration of assimilation rate to a daily total (DTGA)
            self.DTGA += self.FGROS * 3.6

            # integration PAR inside greenhouse to a daily total
            self.DPARDF += self.PARDIF * 3600
            self.DPARDR += self.PARDIR * 3600

        return

    # SUBROUTINE TRUGRO - Calculates SINK STRENGTH of VEGETATIVE UNITS and      *
    # individual FRUIT TRUSSES in tomato
    def trugro(self,day,TMPA,fruit_dev_writer):
        A = 0.1541 / 1.12 * 1.03
        B = 4.3435
        C = 0.2782
        D = 1.3065
        AVTEMP_TRUSS = [0] * 75
        VEGDEV = [0] * 75

        FACSINK = 1.43

        if day < self.STTRU:
            FR = 0
        else:
            # print('TMPA', TMPA)
            FR = (-0.2863 + 0.1454 * math.log(TMPA))* self.CORFR

        self.initial_truss = self.initial_truss + FR
        TRUSS = int(self.initial_truss)

        # C Calculation of sinkstrength of individual trusses
        # C if IAGE(I) < 1 truss was at anthesis today -> sinkstrength = 0
        # C if ITG(I) = 1 truss was already harvested -> sinkstrength = 0

        self.TOTAL = 0
        self.TOTALVEG = 0

        if TRUSS < 1 or (TRUSS == 1 and IAGE[0] < 1):
            self.FLV = self.FRLV
            self.FST = 1.0 - self.FRLV
            self.FSO = 0
            if TRUSS == 1:
                IAGE[0] = IAGE[0] + 1
        else:
            self.NRVEGUNITS = TRUSS + 3
            for i in range(TRUSS):
                if self.ITG[i] == 1 or IAGE[i] < 1:
                    self.SINK[i] = 0
                else:
                    self.DEV[i] = self.DEV[i] + (1.814 + math.log(TMPA / 20.0) * (3.92 - 0.2127 * \
                        self.DEV[i] + 0.004505 * self.DEV[i]**2 - 0.000024 * self.DEV[i]**3)) * self.CORDEV

                    self.TEMP[i] += TMPA
                    AVTEMP_TRUSS[i] = self.TEMP[i]/IAGE[i]
                    # calculation of truss sink strength
                    Y=A * (1 + math.exp(-B * (self.DEV[i] / 100-C)))**(1 / (1-D))
                    if i >= self.TRUSS_POS:
                        self.SINK[i] = self.PLDENS2 * self.NRFRTS[i] * FACSINK * self.FSINK * Y * B / (D-1)\
                        /(math.exp(B * (self.DEV[i] / 100 - C)) + 1)
                    else:
                        self.SINK[i] = self.PLDENS * self.NRFRTS[i] * FACSINK * self.FSINK * Y * B / (D - 1) \
                        / (math.exp(B * (self.DEV[i] / 100 - C)) + 1)

                # TOTAL = total sink strength of generative plant part
                self.TOTAL += self.SINK[i]

            # initiation of vegetative
            if IAGE[0] == 1:
                VEGDEV[0] = 40.
                VEGDEV[1] = 24.
                VEGDEV[2] = 12
            for i in range(self.NRVEGUNITS):
                if self.ITGVEG[i] == 1 or VEGDEV[i] >= 100:
                    self.SINKVEG[i] = 0
                else:
                    VEGDEV[i] = VEGDEV[i] + 1.814 + math.log(TMPA / 20.0) * \
                                (3.92 - 0.2127*VEGDEV[i] + 0.004505*VEGDEV[i]**2\
                                 - 0.000024 * VEGDEV[i] ** 3)
                    # C Calculation of sink strength of vegetative units
                    YVEG = A * (1+math.exp(-B * (VEGDEV[i]/100-C)))**(1/(1-D))
                    if i >= self.VEG_POS:
                        self.SINKVEG[i] = self.PLDENS2 * 3 * self.CORVEGSINK * FACSINK * self.FSINK *\
                            YVEG * B / (D - 1) / (math.exp(B * (VEGDEV[i] / 100 - C)) + 1)
                    else:
                        self.SINKVEG[i] = self.PLDENS * 3 * self.CORVEGSINK * FACSINK * self.FSINK * \
                                          YVEG * B / (D - 1) / (math.exp(B * (VEGDEV[i] / 100 - C)) + 1)

                    if i == 1:
                        self.SINKVEG[i] *= 2.5

                self.TOTALVEG += self.SINKVEG[i]

            # Calculation of vegetative sink strength and total plant sink strength
            self.TOTAL += self.TOTALVEG

            for i in range(TRUSS):
                if self.MANUAL_LEAF_PICKING:
                    if i == 1:
                        self.NRPICKEDUNITS = int(self.lint(self.PDVU, len(self.PDVU),day))
                        for j in range(self.NRPICKEDUNITS):
                            self.ITGVEG[j] = 1
                else:
                    if self.DEV[i] >=  (90 * self.CORBLAD):
                        self.ITGVEG[i] = 1

                if self.DEV[i] >= 100 and self.ITG[i] != 1:
                    self.ITG[i] = 1
                    # write fruit dev! aaronli
                    fruit_dev_writer.writerow([i+1, day, AVTEMP_TRUSS[i], IAGE[i]])
                else:
                    IAGE[i] = IAGE[i] + 1

            self.FLV = self.TOTALVEG/self.TOTAL * self.FRLV
            self.FST = self.TOTALVEG / self.TOTAL * (1 - self.FRLV)
            self.FSO = (self.TOTAL - self.TOTALVEG) / self.TOTAL
        return

    # Calculation of crop growth based on gross photosynthesis	  *
    # *          dry weights of the plant parts, respiration parameters and     *
    # *          dry matter distribution
    def cropgrowth(self,TMPA):

        ITIME = int(self.TIME)
        ISTARTTIM = int(self.start_time)

        # Maintenance respiration [g CH2O m-2 day-1]
        MAINTS = self.CORMAINT * (self.WLVE*self.MAINLV + self.WST*self.MAINST + self.WSOE*self.MAINSO +\
                                  self.WRT*self.MAINRT)
        TEFF = self.Q10**((TMPA - self.REFTMP) / 10)

        if ITIME == ISTARTTIM:
            self.MAINT = min(self.GPHOT, MAINTS * TEFF)

            ASRQ = self.CORGROWTHRESP * (self.FLV * self.ASRQLV + self.FST * self.ASRQST +\
                                         self.FSO * self.ASRQSO + self.FRT * self.ASRQRT )
        # Rate of growth  [g d.w. m-2 day-1]
            self.GTW = (self.GPHOT - self.MAINT) / ASRQ
        self.RGR[ITIME] = self.GTW / (self.WLVE + self.WST + self.WSOE + self.WRT)
        if ITIME >= (ISTARTTIM+4):
            self.RGR_AV =(self.RGR[ITIME] + self.RGR[ITIME - 1] + self.RGR[ITIME - 2] +\
                          self.RGR[ITIME - 3] + self.RGR[ITIME - 4]) / 5
        elif ITIME == ISTARTTIM:
            self.RGR_AV = self.RGR[ITIME]
        else:
            self.RGRSOM += self.RGR[ITIME]
            self.RGR_AV = self.RGRSOM / int(self.TIME - self.start_time)

        MAINT_HELP = MAINTS * TEFF * self.A * (1-math.exp(-self.B * self.RGR_AV))
        self.MAINT = min(self.GPHOT, MAINT_HELP)

        # assimilate requirements for dry matter conversion
        ASRQ = self.CORGROWTHRESP * (self.FLV * self.ASRQLV + self.FST * self.ASRQST + self.FSO * self.ASRQSO\
                                     +self.FRT * self.ASRQRT)

        # rate of growth
        self.GTW = (self.GPHOT - self.MAINT) / ASRQ
        self.GTW += self.BUFFER
        self.TOTAL = self.TOTALVEG * (1 + self.FRTVEG) + (self.TOTAL - self.TOTALVEG)

        # calculation of growth of vegetative plant parts
        TRUSS = int(self.initial_truss)
        if TRUSS < 1 or (TRUSS == 1 and IAGE[0] <= 1):
            GLV = self.FLV * self.GTW
            GST = self.FST * self.GTW
            GRT = self.FRT * self.GTW
            GSO = 0
        else:
            for i in range(self.NRVEGUNITS):
                if self.TOTAL >= self.GTW:
                    self.GRVEG[i] = self.SINKVEG[i] / self.TOTAL * self.GTW
                else:
                    self.GRVEG[i] = self.SINKVEG[i]

            if self.TOTAL >= self.GTW:
                GRT = self.GTW * self.FRT
                GLV = self.GTW * self.FLV
                GST = self.GTW * self.FST
                self.BUFFER = 0
            else:
                GRT = self.TOTALVEG / (1. - self.FRTVEG) * self.FRTVEG
                GLV = self.TOTALVEG * self.FRLV
                GST = self.TOTALVEG * (1. - self.FRLV)
                BUFFER = self.GTW - self.TOTAL

            # calculation of growth of individual trusses
            GSO = 0
            for i in range(TRUSS):
                if self.TOTAL >= self.GTW:
                    self.GRTRUSS[i] = self.SINK[i] / self.TOTAL * self.GTW
                else:
                    self.GRTRUSS[i] = self.SINK[i]
                GSO += self.GRTRUSS[i]

        if not self.FIXEDCROP:
            for i in range(TRUSS):
                self.WTRUSS[i] = self.WTRUSS[i] + self.GRTRUSS[i]
            for i in range(self.NRVEGUNITS):
                self.WVEGUNIT[i] += self.GRVEG[i]
            self.WRT += GRT
            self.WLV += GLV
            self.WST += GST
            self.WSO += GSO
            self.GTW = GLV + GST + GSO + GRT
            self.WSTE = self.WST
            self.WSOR = 0
            for i in range(TRUSS):
                if self.ITG[i] != 1:
                    self.WSOE += self.WTRUSS[i]
            WLVPICKED = 0
            if not self.MANUAL_LEAF_PICKING:
        # First veg. unit will be picked in two sessions
                if (self.DEV[0] >= 70*self.CORBLAD) and (self.DEV[0] < (90*self.CORBLAD)):
                    WLVPICKED = self.WVEGUNIT[0] * 0.7 / 2.0
                else:
                    for i in range(self.NRVEGUNITS):
                        if self.ITGVEG[i] == 1:
                            WLVPICKED += self.WVEGUNIT[i] * 0.7
            else:
                for i in range(self.NRVEGUNITS):
                    if self.ITGVEG[i] == 1:
                        WLVPICKED += self.WVEGUNIT[i] * 0.7

            self.NRPICKEDUNITS = 0
            for i in range(self.NRVEGUNITS):
                if self.ITGVEG[i] == 1:
                    self.NRPICKEDUNITS += 1

            self.WLVE = self.WLV - WLVPICKED
            # problem with non-define variable
            # self.HARVEST = self.HARVEST / 55

            self.WTW = self.WLV + self.WST + self.WRT

        return

    def printout_growth(self, writer, AVRAD, CO2, TMPA, SLA,fruit_writer):
        # print("This is time {} and this is start time {} and icount {}".format(self.TIME, self.start_time, self.ICOUNT))
        if self.TIME == self.start_time:
            headrow = ['Time(jday)','AVRAD(MJ/m2/d)','Temperature(oC)','CO2','FGMAX(mgCO2/m2/s)','EFF(mgCO2/J)','SLA*10000',\
                       'LAI', 'GPHOT (gCH2O/m2/d)','RGR_AV(1/d)','MAINT(gCH2O/m2/d)','GTW(g/m2/d)','WTW(g/m2)',\
                       'WTW-WRT(g/m2)','WLV(g/m2)','WLV+WST(g/m2)','WSO(g/m2)','WRT(g/m2)','WLVE(g/m2)','WSTE(g/m2)',\
                       'WSOE(g/m2)','DPARDF(MJ/m2/d)','DPARDR(MJ/m2/d)']
            writer.writerow(headrow)
            fruit_dev_headrow = ['TRNR','DAY','AVTEMP','IAGE']
            fruit_writer.writerow(fruit_dev_headrow)

        if self.TIME == self.start_time or self.ICOUNT == self.PRDEL or self.TIME == self.finish_time:
            # print("do you know me {} and {}".format(self.ICOUNT,self.TIME))
            datarow= [self.TIME, AVRAD / 1000000, TMPA, CO2, self.FGMAX, self.EFF, SLA * 10000,self.LAI, self.GPHOT\
                      , self.RGR_AV, self.MAINT, self.GTW, self.WTW, self.WTW - self.WRT, self.WLV, self.WLV+self.WST\
                      , self.WSO, self.WRT, self.WLVE, self.WSTE, self.WSOE, self.DPARDF/1000000, self.DPARDR/1000000]
            for i in range(len(datarow)):
                datarow[i] = round(datarow[i],2)
            self.ICOUNT = 0
            writer.writerow(datarow)

        self.ICOUNT += 1
        return

    def printout_distri(self, writer, SLA, GTWOLD, TMPA, CO2):
        if self.TIME == self.start_time:
            headrow = ['Time(jday)','FRVEG','TOTALVEG','TOTAL','SLA * 10000','GTWOLD','WTW',\
                       'WLV', 'WST','WSO','BUFFER','TRNR','TMPA',\
                       'CO2','NRVEGUNITS']
            for i in range(1,36):
                headrow.append('TRUSS_'+ str(i))
            headrow.append('WTRUSS_615')
            for i in range(1,17):
                headrow.append('WVEGUNIT_' + str(i))
            writer.writerow(headrow)

        if self.TIME == self.start_time or self.ICOUNT1 == self.PRDEL or self.TIME == self.finish_time:
            datarow = [self.TIME, (self.FLV/self.FST)/(self.FLV + self.FST + self.FSO), self.TOTALVEG, self.TOTAL,\
                       SLA * 10000, GTWOLD, self.WTW, self.WLV, self.WST,self.WSO, self.BUFFER, self.initial_truss,\
                       TMPA, CO2, self.NRVEGUNITS]
            for i in range(35):
                datarow.append(self.WTRUSS[i])
            datarow.append(self.WTRUSS615)
            for i in range(16):
                datarow.append(self.WVEGUNIT[i])
            self.ICOUNT1 = 0
            # decimal accuracy
            for i in range(len(datarow)):
                datarow[i] = round(datarow[i],2)
            writer.writerow(datarow)

        self.ICOUNT1 += 1


    def start_simulation(self):
        # pre-simulation
        output_growth = os.path.abspath(os.path.join(os.getcwd(),'static/tomsim_growth.csv'))
        output_distri = os.path.abspath(os.path.join(os.getcwd(),'static/tomsim_distri.csv'))
        output_FruitDev = os.path.abspath(os.path.join(os.getcwd(),'static/tomsim_FruitDev.csv'))
        f_growth = open(output_growth,'w',encoding='utf-8',newline="")
        f_distri = open(output_distri, 'w', encoding='utf-8', newline="")
        f_fruitdev = open(output_FruitDev, 'w', encoding='utf-8', newline="")
        growth_writer = csv.writer(f_growth)
        distri_writer = csv.writer(f_distri)
        fruitdev_writer = csv.writer(f_fruitdev)

        self.pre_simulation()
        while self.TIME <= self.finish_time:
            itime = self.TIME
            # calculate Julian day number from TIME
            day = (self.TIME - 1) % 365 + 1
            AVRAD = 0
            DGLOSTAB = self.GLOSTAB[itime - 1] * self.CORRADIANCE
            for i in range(24):
                self.GLOB[i] = self.GLOTAB[itime - 1][i] * self.CORRADIANCE
                self.DTEMP[i] = self.TEMPTAB[itime - 1][i] * self.CORTEMP
                self.DCO2[i] = self.CO2TAB[itime - 1][i] * self.CORCO2
                AVRAD += self.GLOB[i] * 3600
            TMPA = self.AVTEMP[itime - 1] * self.CORTEMP
            CO2 = self.CO2D[itime - 1]
            # calculate LAI
            if self.LAICALC:
                if self.SLAFUNCT:
                    SLA = (266 + 88 * math.sin(2 * PI * (day + 68) / 365)) / 10000
                else:
                    SLA = self.lint(self.SLAT, self.ISLAT, self.TIME) / 10000
                SLA *= self.CORSLA
                self.LAI = SLA * self.WLVE
            else:
                self.LAI = self.lint(self.LAIT, self.ILAIT, self.TIME)

            # calculate dry matter distribution ratios
            self.FRTVEG = 0.15

            LATRAD = LAT * PI / 180

            # This subroutine calculates astronomic daylength ad diuranal radiation ...
            self.astrog(day, LATRAD)

            # crop growth -----------------------------------------------------------

            # Gross assimilation [g CO2 m-2 day-1]
            self.totass(day)

            # gross photosynthesis [g CH2O m-2 day-1]
            self.GPHOT = self.DTGA * 34 / 44

            # Is there a side shoot?
            if self.SIDE_SHOOT:
                if day >= self.DATE_FLOWER_SHOOT and not self.INITATION:
                    self.TRUSS_POS = int(self.initial_truss)
                    # problem with NRVEGUNITS   aaronli
                    self.VEG_POS = self.NRVEGUNITS - 3
                    self.INITATION = True

            self.trugro(day, TMPA, fruitdev_writer)

            FRACTIONS = (self.FLV + self.FST) * (1 + self.FRTVEG) + self.FSO
            self.FRT = self.FRTVEG * (self.FLV+ self.FST) / FRACTIONS
            self.FLV = self.FLV / FRACTIONS
            self.FST = self.FST / FRACTIONS
            self.FSO = self.FSO / FRACTIONS

            self.cropgrowth(TMPA)
            for i in range(6-1,int(self.initial_truss)):
                self.WTRUSS615 += self.GRTRUSS[i]

            # output during simulation
            self.printout_growth(growth_writer, AVRAD, CO2, TMPA, SLA, fruitdev_writer)
            GTWOLD = self.GTW
            self.printout_distri(distri_writer, SLA, GTWOLD, TMPA, CO2)

            self.TIME += self.DELT
        f_growth.close()
        f_distri.close()

        GEMEIND1 = 0
        for i in range(30):
            GEMEIND1 += self.WTRUSS[i]/30
        GEMEIND1 = GEMEIND1 / self.PLDENS / self.NRFRT / self.CORNRFRTS
        fruitdev_writer.writerow(['Avg final truss DW 1-30', round(GEMEIND1, 2)])
        ITRUSS = int(self.initial_truss)
        GEMEIND2 = 0
        fruitdev_writer.writerow(['Final truss number', ITRUSS])

        for i in range(ITRUSS):
            GEMEIND2 += self.WTRUSS[i]/ITRUSS
        GEMEIND2 = GEMEIND2 / self.PLDENS/ self.NRFRT / self.CORNRFRTS
        fruitdev_writer.writerow(['Avg truss DW', GEMEIND2])


        f_fruitdev.close()

        return
