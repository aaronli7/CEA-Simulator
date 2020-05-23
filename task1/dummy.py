jsonStringParsed=jsonString.replace("\'", "\"")
jsonStringParsed1=jsonStringParsed.replace(" ", "")
data=json.loads(jsonStringParsed1)
jsonDf=pd.read_json(jsonStringParsed1)
timeSeriesValues=jsonDf['time'].values
timeSeries=[]
timeSeriesEpoch=[]
for item in range(len(timeSeriesValues)):
    timestamp=datetime.strptime(timeSeriesValues[item],"%Y-%m-%dT%H:%M:%SZ").timestamp()
    timeSeriesEpoch.insert(item,int(timestamp))
print ('Start Epoch Time: {} ; End Epoch Time: {}'.format(min(timeSeriesEpoch),max(timeSeriesEpoch)))
