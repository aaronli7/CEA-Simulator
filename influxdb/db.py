import pandas as pd
from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('db1')

df=pd.read_csv('Final.csv')

for row_ind, r in df.iterrows():
    dbname = "Mapdata1"
    json_body = [
        {
            "measurement": dbname,
            "fields": {

                "id": r[0],
                "latitude": r[1],
                "longitude": r[2]
            }
        }
    ]
    client.write_points(json_body)